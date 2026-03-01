import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title(" Burnout Intelligence System")

if "token" not in st.session_state:
    st.session_state.token = None

menu = st.sidebar.selectbox("Menu", ["Register", "Login", "Predict", "History"])


if menu == "Register":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        r = requests.post(f"{API_URL}/register", json={
            "email": email,
            "password": password
        })
        st.write(r.json())


elif menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        r = requests.post(f"{API_URL}/login", json={
            "email": email,
            "password": password
        })
        data = r.json()
        if "access_token" in data:
            st.session_state.token = data["access_token"]
            st.success("Login Successful")
        else:
            st.error("Login Failed")

elif menu == "Predict":

    if not st.session_state.token:
        st.warning("Please login first")
    else:
        attendance = st.slider("Attendance", 0, 100, 75)
        assignment_rate = st.slider("Assignment Completion %", 0, 100, 70)
        study_hours = st.slider("Study Hours", 0, 12, 5)
        sleep_hours = st.slider("Sleep Hours", 0, 12, 6)
        screen_time = st.slider("Screen Time", 0, 12, 4)
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
        mood_score = st.slider("Mood Score (1-10)", 1, 10, 6)
        previous_gpa = st.slider("Previous GPA", 0.0, 10.0, 7.5)

        if st.button("Predict Burnout"):

            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            r = requests.post(
                f"{API_URL}/predict",
                headers=headers,
                json={
                    "attendance": attendance,
                    "assignment_rate": assignment_rate,
                    "study_hours": study_hours,
                    "sleep_hours": sleep_hours,
                    "screen_time": screen_time,
                    "stress_level": stress_level,
                    "mood_score": mood_score,
                    "previous_gpa": previous_gpa
                }
            )

            result = r.json()

            st.metric("Burnout %", result["risk_percentage"])
            st.write("Risk Level:", result["risk_level"])

            if result["alert"]:
                st.error(" Repeated High Burnout Detected")

            st.markdown("### 🧠 AI Advice")
            st.write(result["advice"])

elif menu == "History":

    if not st.session_state.token:
        st.warning("Please login first")
    else:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.get(f"{API_URL}/history", headers=headers)
        st.write(r.json())