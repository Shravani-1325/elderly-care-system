import streamlit as st
import pandas as pd
import plotly.express as px
import json
import psycopg2
import requests
from agents.user_utils import get_user_ids

st.set_page_config(
    page_title="Elderly Care Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Sidebar
st.sidebar.title("🏥 Health Monitoring Dashboard")
page = st.sidebar.radio("Navigate", ["Dashboard", "Health Monitoring", "Safety Monitoring", "Daily Reminders"])
st.sidebar.markdown("---")

# PostgreSQL Connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="elderly_care",
        user="postgres",
        password="system",
        port=5432
    )

# Fetching user IDs from database using agent function
try:
    user_ids = get_user_ids()
except Exception as e:
    st.sidebar.error(f"❌ Failed to fetch users: {e}")
    user_ids = ["No Users"]

user_id = st.sidebar.selectbox("Select User", user_ids)
st.sidebar.write(f"👤 Selected: {user_id}")

# API Endpoints
HEALTH_API = f"http://localhost:5001/health/user/{user_id}"
SAFETY_API = f"http://localhost:5001/safety/user/{user_id}"
DAILY_API = f"http://localhost:5001/reminders/user/{user_id}"

# Safe JSON fetch function
def safe_get_json(url, key):
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            return response.json().get(key, [])
        else:
            st.error(f"❌ Failed to fetch from API: {url}")
            return []
    except ValueError:
        st.error(f"❌ Invalid JSON from API: {url}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return []

# Dashboard Overview
if page == "Dashboard":
    st.title("📊 Overview Dashboard")
    st.markdown("#### Fetching data from API...")

    health_data = safe_get_json(HEALTH_API, 'health_monitoring')
    health_df = pd.DataFrame([health_data]) if isinstance(health_data, dict) else pd.DataFrame(health_data)

    if not health_df.empty:
        st.markdown("### 🧠 Vital Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_hr = health_df['heart_rate'].mean()
            st.metric("❤️ Avg Heart Rate", f"{avg_hr:.1f} bpm")

            # Heart rate zone prediction
            if avg_hr < 60:
                hr_status = "🟦 Low"
            elif 60 <= avg_hr <= 100:
                hr_status = "🟩 Normal"
            elif 101 <= avg_hr <= 120:
                hr_status = "🟧 Elevated"
            else:
                hr_status = "🟥 High"

            st.markdown(f"**Predicted Status:** {hr_status}")
        with col2:
            st.metric("💉 Avg BP Systolic", f"{health_df['bp_systolic'].mean():.1f}")
        with col3:
            st.metric("🌡️ Avg Temp", f"{health_df['temperature'].mean():.1f} °C")

        st.subheader("🫀 Bubble Chart: BP vs Temp (Heart Rate Zones)")

      
        health_df['hr_zone'] = pd.cut(health_df['heart_rate'], bins=[0, 60, 80, 100, 200],
                                    labels=["Low", "Normal", "Elevated", "High"])

        fig = px.scatter(
            health_df, x="bp_systolic", y="temperature",
            size="bp_diastolic", color="hr_zone",
            title="BP vs Temp colored by Heart Rate Zone",
            labels={"hr_zone": "Heart Rate Zone"}
        )
        st.plotly_chart(fig)
    else:
        st.markdown("### ⚠️ No Health Data Found")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("❤️ Avg Heart Rate", "N/A")
        with col2:
            st.metric("💉 Avg BP Systolic", "N/A")
        with col3:
            st.metric("🌡️ Avg Temp", "N/A")
        st.warning("⚠️ No health data available for the selected user. Please ensure the backend API is running and data exists.")
        st.info("ℹ️ Tip: Go to the Health Monitoring tab for real-time logs or try a different user from the sidebar.")

# Health Monitoring Page
elif page == "Health Monitoring":
    st.title("❤️ Health Monitoring")
    health_data = safe_get_json(HEALTH_API, 'health_monitoring')
    health_df = pd.DataFrame([health_data]) if isinstance(health_data, dict) else pd.DataFrame(health_data)
    st.dataframe(health_df)

    if not health_df.empty:
        if not health_df.empty:
            st.subheader("🧠 Heart Rate Status Prediction")

            avg_hr = health_df['heart_rate'].mean()

            # Predict the status
            if avg_hr < 60:
                hr_status = "🟦 Low"
            elif 60 <= avg_hr <= 100:
                hr_status = "🟩 Normal"
            elif 101 <= avg_hr <= 120:
                hr_status = "🟧 Elevated"
            else:
                hr_status = "🟥 High"

            st.markdown(f"**Average Heart Rate:** `{avg_hr:.1f} bpm`")
            st.markdown(f"**Predicted Status:** {hr_status}")

        st.subheader("📊 Vital Signs Correlation")
        fig = px.scatter_matrix(health_df,
            dimensions=["bp_systolic", "bp_diastolic", "heart_rate", "temperature"],
            color="heart_rate",
            title="Correlation Between Vitals")
        st.plotly_chart(fig)

        st.subheader("📉 Trends Over Time")
        melted_df = health_df.melt(id_vars="timestamp", value_vars=["heart_rate", "bp_systolic", "bp_diastolic", "temperature"],
                                var_name="Vital Sign", value_name="Value")

        fig_time = px.bar(
            melted_df,
            x="timestamp",
            y="Value",
            color="Vital Sign",
            barmode="group",
            title="Vital Signs Over Time (Grouped Bars)"
        )
        st.plotly_chart(fig_time)

# Safety Monitoring Page
elif page == "Safety Monitoring":
    st.title("🛡️ Safety Monitoring")
    try:
        response = requests.get(SAFETY_API)
        if response.status_code == 200 and response.content:
            safety = response.json().get('safety_monitoring')
            if safety:
                st.subheader("🚨 Safety Alert Details")
                st.markdown(f"**📅 Time:** {safety.get('timestamp', 'N/A')}")
                st.markdown(f"**📍 Location:** {safety.get('location', 'N/A')}")
                st.markdown(f"**⚠️ Event Type:** `{safety.get('event_type', 'N/A')}`")
                st.markdown(f"**📞 Emergency Call Triggered:** {'✅ Yes' if safety.get('emergency_call') else '❌ No'}")
                st.markdown(f"**🛑 Unsafe Detected:** {'🟥 Yes' if safety.get('unsafe') else '🟩 No'}")

                st.subheader("📊 Emergency Call Summary")
                emergency_df = pd.DataFrame({
                    "Type": ["Emergency Call", "No Call"],
                    "Count": [1 if safety.get('emergency_call') else 0, 1 if not safety.get('emergency_call') else 0]
                })
                fig = px.pie(emergency_df, names="Type", values="Count", title="Emergency Call Ratio")
                st.plotly_chart(fig)

                st.subheader("📍 Event Type Breakdown")
                event_df = pd.DataFrame({"Event Type": [safety.get('event_type')], "Count": [1]})
                fig_event = px.bar(event_df, x="Event Type", y="Count", title="Type of Events Detected")
                st.plotly_chart(fig_event)

                if safety.get('unsafe'):
                    st.error("🔴 Alert! Unsafe condition detected!")
                else:
                    st.success("🟢 All clear.")
            else:
                st.warning("⚠️ No safety data found.")
        else:
            st.error("❌ No safety data found.")
    except Exception as e:
        st.error(f"❌ Error fetching safety data: {e}")

# Daily Reminders Page
elif page == "Daily Reminders":
    st.title("⏰ Daily Reminders")
    try:
        response = requests.get(DAILY_API)
        if response.status_code == 200 and response.content:
            reminder = response.json().get('daily_reminders')
            if reminder:
                df = pd.DataFrame([reminder])
                st.dataframe(df)
                st.subheader("🔁 Reminder Summary")
                st.markdown(f"📌 **Task:** {reminder.get('task', 'N/A')}")
                st.markdown(f"🕒 **From:** {reminder.get('start_time', 'N/A')} → **To:** {reminder.get('end_time', 'N/A')}")
                st.markdown(f"📤 **Reminder Sent:** {'✅ Yes' if reminder.get('reminder_sent') else '❌ No'}")
                st.markdown(f"☑️ **Acknowledged:** {'✅ Yes' if reminder.get('acknowledged') else '❌ No'}")

                summary_df = pd.DataFrame({
                    "Acknowledged": [int(reminder.get('acknowledged'))],
                    "Missed": [int(not reminder.get('acknowledged'))]
                })
                st.subheader("📈 Acknowledgement Trend")
                fig_summary = px.bar(summary_df.melt(), x="variable", y="value", color="variable", title="Acknowledged vs Missed")
                st.plotly_chart(fig_summary)
            else:
                st.markdown("### 😴 No Active Reminders")
                st.info("💡 Encourage regular routines and suggest setting new reminders.")
                st.warning("📭 This user currently has no scheduled tasks. Let's create something meaningful!")
        else:
            st.markdown("### ❌ Failed to Fetch Reminder Data")
            st.warning("🚧 We're having trouble connecting to the reminder service. Please try again shortly or check your server.")
    except Exception as e:
        st.error(f"❌ Error fetching reminders: {e}")
        
        
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #cfcfcf;
    }
    .stButton button {
        background-color: #6C63FF;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #7b72ff;
    }
    </style>
""", unsafe_allow_html=True)
      
