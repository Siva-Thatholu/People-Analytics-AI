import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="HR Flight Risk Dashboard", layout="wide")
st.title("🧠 AI-Driven People Analytics Dashboard")

with st.sidebar:
    st.header("Admin Controls")
    if st.button("Generate Synthetic Data (Run NLP)"):
        with st.spinner("Generating data and calling Gemini API..."):
            try:
                res = requests.post(f"{API_URL}/api/generate?num_records=50")
                st.success(res.json().get("message", "Success"))
            except Exception as e:
                st.error("Make sure FastAPI backend is running!")

try:
    employees_res = requests.get(f"{API_URL}/api/employees")
    if employees_res.status_code == 200 and len(employees_res.json()) > 0:
        df = pd.DataFrame(employees_res.json())

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Employees Analyzed", len(df))
        col2.metric("High Flight Risk Employees", len(df[df["flight_risk"] == "High"]))
        col3.metric("Average Company Sentiment", f"{df['sentiment_score'].mean():.2f} / 1.0")

        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Flight Risk by Department")
            risk_fig = px.histogram(df, x="department", color="flight_risk", 
                                    color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"},
                                    barmode="group")
            st.plotly_chart(risk_fig, use_container_width=True)

        with col_chart2:
            st.subheader("Top Turnover Themes (NLP Extracted)")
            theme_counts = df['key_theme'].value_counts().reset_index()
            theme_counts.columns = ['Theme', 'Count']
            theme_fig = px.pie(theme_counts, names='Theme', values='Count', hole=0.4)
            st.plotly_chart(theme_fig, use_container_width=True)

        st.subheader("Raw Employee Survey Data & Sentiment")
        st.dataframe(df[["employee_id", "department", "survey_feedback", "sentiment_score", "key_theme", "flight_risk"]])

    else:
        st.info("No data found. Click 'Generate Synthetic Data' in the sidebar to populate the database.")
except Exception as e:
    st.error("Failed to connect to the backend. Is FastAPI running?")
