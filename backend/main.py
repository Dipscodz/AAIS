from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
import numpy as np

from backend.database import engine, SessionLocal
from backend.models_db import Base, User, Prediction
from backend.schemas import StudentData, UserCreate, UserLogin
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from backend.model_loader import model, scaler
from backend.llm_service import generate_burnout_advice

app = FastAPI(title="AAIS Burnout Intelligence System")

Base.metadata.create_all(bind=engine)


# -------------------------
# Database Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# -------------------------
# Login
# -------------------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# Predict Burnout
# -------------------------
@app.post("/predict")
def predict(
    data: StudentData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    input_data = np.array([[ 
        data.attendance,
        data.assignment_rate,
        data.study_hours,
        data.sleep_hours,
        data.screen_time,
        data.stress_level,
        data.mood_score,
        data.previous_gpa
    ]])

    input_scaled = scaler.transform(input_data)

    probability = model.predict_proba(input_scaled)[0][1]
    probability = float(probability)

    if probability > 0.7:
        risk = "High"
    elif probability > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    advice = generate_burnout_advice(
        user_data=data.dict(),
        risk_level=risk,
        risk_score=round(probability * 100, 2)
    )

    new_prediction = Prediction(
        burnout_probability=probability,
        risk_level=risk,
        advice=advice,
        user_id=current_user.id
    )

    db.add(new_prediction)
    db.commit()

    # Check last 3 predictions
    recent = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(desc(Prediction.id)).limit(3).all()

    high_count = sum(1 for r in recent if r.risk_level == "High")
    alert = True if high_count >= 3 else False

    return {
        "burnout_probability": probability,
        "risk_level": risk,
        "risk_percentage": round(probability * 100, 2),
        "alert": alert,
        "advice": advice
    }


# -------------------------
# Prediction History
# -------------------------
@app.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(desc(Prediction.id)).all()

    return predictions