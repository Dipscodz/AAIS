import streamlit as st
import requests


st.set_page_config(page_title="AAIS - Burnout Detection", layout="centered")

st.title("🎓 Autonomous Academic Intelligence System")
st.subheader("Student Burnout Risk Prediction")

st.markdown("---")



attendance = st.slider("Attendance (%)", 0, 100, 75)
assignment_rate = st.slider("Assignment Completion Rate (%)", 0, 100, 80)
study_hours = st.slider("Daily Study Hours", 0.0, 12.0, 5.0)
sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 6.0)
screen_time = st.slider("Screen Time (hours)", 0.0, 12.0, 6.0)
stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
mood_score = st.slider("Mood Score (1-10)", 1, 10, 6)
previous_gpa = st.slider("Previous GPA", 0.0, 10.0, 7.0)

st.markdown("---")



if st.button("Predict Burnout Risk"):

    data = {
        "attendance": attendance,
        "assignment_rate": assignment_rate,
        "study_hours": study_hours,
        "sleep_hours": sleep_hours,
        "screen_time": screen_time,
        "stress_level": stress_level,
        "mood_score": mood_score,
        "previous_gpa": previous_gpa
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data
        )

        result = response.json()

        probability = result["burnout_probability"]
        risk = result["risk_level"]

        st.markdown("## 🔎 Prediction Result")

        st.metric("Burnout Probability", f"{probability:.2f}")

        if risk == "High":
            st.error(f"Risk Level: {risk}")
        elif risk == "Medium":
            st.warning(f"Risk Level: {risk}")
        else:
            st.success(f"Risk Level: {risk}")

    except:
        st.error(" Backend not running. Please start FastAPI server.")