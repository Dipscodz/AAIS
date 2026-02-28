from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models_db import Base, User, Prediction
from .schemas import StudentData, UserCreate, UserLogin
from .auth import hash_password, verify_password, create_access_token
from .model_loader import model, scaler
import numpy as np

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AAIS SaaS Backend")


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


    
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token}


# -------------------
# Predict + Save History
# -------------------
@app.post("/predict/{user_id}")
def predict(user_id: int, data: StudentData, db: Session = Depends(get_db)):

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

    if probability > 0.7:
        risk = "High"
    elif probability > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    new_prediction = Prediction(
        burnout_probability=float(probability),
        risk_level=risk,
        user_id=user_id
    )

    db.add(new_prediction)
    db.commit()

    return {
        "burnout_probability": float(probability),
        "risk_level": risk
    }


# -------------------
# Get User History
# -------------------
@app.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):

    predictions = db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).all()

    return predictions