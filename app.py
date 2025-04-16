import streamlit as st
import datetime
from utils.weather_utils import fetch_weather_features, map_weather_features
from utils.alert_utils import send_alert_to_capitol_hotel
import joblib
import base64
import os

# --- Global Styling (Applies to both pages) ---
st.markdown(
    """
    <style>
    .stApp {
        color: #703900;
    }
    html, body, [class*="st-"], .stApp * {
        color: #703900 !important;
    }
    .stDateInput input {
        background-color: white !important;
        color: #703900 !important;
        border: 1px solid #703900 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
    }
    .stDateInput > div {
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #703900 !important;
    }
    .stButton > button {
        background-color: white !important;
        color: #703900 !important;
        border: 1px solid #703900 !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
    }
    .stAlert {
        background-color: white !important;
        color: #703900 !important;
        border-left: 5px solid #703900 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Background Setter ---
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Login Page ---
def login():
    set_background("assets/background.jpg")

    st.markdown("""
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-inner {
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 300px;
        }
        input[type="text"], input[type="password"] {
            background-color: white !important;
            border-radius: 12px !important;
            height: 60px !important;
            padding: 12px !important;
            font-size: 1.1rem !important;
            border: 2px solid #703900 !important;
        }
        .stButton > button {
            margin: auto;
            background-color: white !important;
            color: #703900 !important;
            border: 2px solid #703900 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-size: 1rem !important;
        }
        </style>

        <div class="login-container">
            <div class="login-inner">
        """, unsafe_allow_html=True)

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    login_btn = st.button("Login")

    st.markdown("</div></div>", unsafe_allow_html=True)

    if login_btn:
        if email == "praneethaimandi@gmail.com" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Wrong credentials")

# --- Main App Page ---
def predictor_app():
    set_background("assets/prediction.jpg")

    FULL_CAPACITY = 93470
    MODEL_FEATURES = [
        'cloudcover', 'humidity', 'precipcover', 'dew', 'winddir', 'windgust',
        'temp', 'tempmax', 'tempmin', 'windspeed', 'precip'
    ]

    st.title("🔔 Mettur Dam Storage Predictor & Alert System")

    if "alert_sent" not in st.session_state:
        st.session_state.alert_sent = False

    date = st.date_input("📅 Select a date to predict dam storage", datetime.date.today())

    if st.button("Predict Storage"):
        with st.spinner("Fetching weather data and predicting..."):
            st.session_state.alert_sent = False

            weather_data = fetch_weather_features(date, "mettur")
            mapped = map_weather_features(weather_data, "mettur")

            model = joblib.load("models/storage_mettur_model.pkl")
            features = [mapped.get(feat, 0) for feat in MODEL_FEATURES]
            predicted_storage = model.predict([features])[0]

            percent = (predicted_storage / FULL_CAPACITY) * 100
            release = 0.0
            zone = ""

            if percent >= 93:
                zone = "🟥 RED ZONE"
                release = predicted_storage - (FULL_CAPACITY * 0.93)
            elif 85 <= percent < 93:
                zone = "🟨 Yellow Zone"
            else:
                zone = "🟩 Green Zone"
                if not st.session_state.alert_sent:
                    send_alert_to_capitol_hotel()
                    st.session_state.alert_sent = True

            st.success(f"📦 Predicted Storage: {predicted_storage:.2f} M.Cft.")
            st.info(f"📊 Storage as % of capacity: {percent:.2f}%")
            st.warning(f"🚨 Zone Classification: {zone}")
            st.info(f"🌊 Recommended release: {release:.2f} M.Cft.")

# --- Routing ---
if not st.session_state.logged_in:
    login()
else:
    predictor_app()
