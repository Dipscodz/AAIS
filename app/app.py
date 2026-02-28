import streamlit as st
import requests

st.title("🧠 AAIS - Academic Risk System")

attendance = st.slider("Attendance %", 60, 100, 80)
assignment = st.slider("Assignment Completion %", 50, 100, 75)
study = st.slider("Study Hours", 1, 10, 5)
sleep = st.slider("Sleep Hours", 4, 9, 7)
screen = st.slider("Screen Time", 1, 10, 5)
stress = st.slider("Stress Level", 1, 10, 5)
mood = st.slider("Mood Score", 1, 10, 5)
gpa = st.slider("Previous GPA", 5.0, 10.0, 7.5)

if st.button("Predict Burnout Risk"):

    payload = {
        "attendance": attendance,
        "assignment_rate": assignment,
        "study_hours": study,
        "sleep_hours": sleep,
        "screen_time": screen,
        "stress_level": stress,
        "mood_score": mood,
        "previous_gpa": gpa
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    result = response.json()

    st.subheader("Prediction Result")
    st.write(f"Probability: {result['burnout_probability']*100:.2f}%")

    if result["risk_level"] == "HIGH":
        st.error("⚠️ HIGH RISK")
    elif result["risk_level"] == "MODERATE":
        st.warning("⚡ MODERATE RISK")
    else:
        st.success("✅ LOW RISK")