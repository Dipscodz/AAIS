import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AAIS", layout="centered")


if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None





def login_page():
    st.title(" AAIS Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password},
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]

        
            st.session_state.user_id = 1

            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")


def register_page():
    st.title("📝 Register")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"email": email, "password": password},
        )

        if response.status_code == 200:
            st.success("Account created! Please login.")
        else:
            st.error(response.json()["detail"])


def dashboard():

    st.title(" AAIS Dashboard")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.user_id = None
        st.rerun()

    st.markdown("---")

    st.subheader("Burnout Prediction")

    attendance = st.slider("Attendance (%)", 0, 100, 75)
    assignment_rate = st.slider("Assignment Rate (%)", 0, 100, 80)
    study_hours = st.slider("Study Hours", 0.0, 12.0, 5.0)
    sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 6.0)
    screen_time = st.slider("Screen Time", 0.0, 12.0, 6.0)
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    mood_score = st.slider("Mood Score (1-10)", 1, 10, 6)
    previous_gpa = st.slider("Previous GPA", 0.0, 10.0, 7.0)

    if st.button("Predict"):

        data = {
            "attendance": attendance,
            "assignment_rate": assignment_rate,
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "screen_time": screen_time,
            "stress_level": stress_level,
            "mood_score": mood_score,
            "previous_gpa": previous_gpa,
        }

        response = requests.post(
            f"{BACKEND_URL}/predict/{st.session_state.user_id}",
            json=data,
        )

        result = response.json()

        st.metric("Burnout Probability", f"{result['burnout_probability']:.2f}")
        st.write("Risk Level:", result["risk_level"])

    st.markdown("---")
    st.subheader("📊 Prediction History")

    history_response = requests.get(
        f"{BACKEND_URL}/history/{st.session_state.user_id}"
    )

    if history_response.status_code == 200:
        history_data = history_response.json()

        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df)
        else:
            st.info("No history yet.")


if st.session_state.token is None:

    page = st.sidebar.selectbox("Select", ["Login", "Register"])

    if page == "Login":
        login_page()
    else:
        register_page()

else:
    dashboard()