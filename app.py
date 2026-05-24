import streamlit as st
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Institutional Analytics Dashboard",
    layout="wide"
)

# TITLE
st.title("Institutional Analytics Dashboard")

st.write(
    "Executive decision-support dashboard for higher education analytics."
)

# LOAD DATA
df = pd.read_excel("Faculty Enrolment.xlsx")

# KPI SECTION
st.subheader("Key Institutional Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Enrolments",
        int(df["ActualHeadcount"].sum())
    )

with col2:
    st.metric(
        "Total Graduates",
        int(df["Graduates"].sum())
    )

with col3:
    st.metric(
        "Average Success Rate",
        f"{round(df['SuccessRate'].mean(), 2)}%"
    )

# DATA PREVIEW
st.subheader("Dataset Preview")

st.write(df.head())

# DATA GOVERNANCE
st.subheader("Data Governance Checks")

st.write("Missing Values")
st.write(df.isnull().sum())

st.write("Duplicate Records")
st.write(df.duplicated().sum())
