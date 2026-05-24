import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Institutional Analytics Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Institutional Analytics Dashboard")

st.write(
    """
    Executive decision-support dashboard for higher education
    strategic planning, institutional performance monitoring,
    governance, and predictive analytics.
    """
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_excel("Faculty Enrolment.xlsx")

# ---------------------------------------------------
# EXECUTIVE KPI SECTION
# ---------------------------------------------------

st.header("Executive Institutional Overview")

col1, col2, col3, col4, col5 = st.columns(5)

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

with col4:
    st.metric(
        "Research Outputs",
        round(df["ResearchOutputUnits"].sum(), 2)
    )

with col5:
    st.metric(
        "Average Dropout Rate",
        f"{round(df['DropoutRate'].mean(), 2)}%"
    )

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

faculty_filter = st.sidebar.selectbox(
    "Select Faculty",
    ["All"] + list(df["Faculty"].unique())
)

if faculty_filter != "All":
    df = df[df["Faculty"] == faculty_filter]

# ---------------------------------------------------
# ENROLMENT ANALYTICS
# ---------------------------------------------------

st.header("Institutional Performance Analytics")

# Enrolment Trends
enrolment_trend = (
    df.groupby("Year")["ActualHeadcount"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    enrolment_trend,
    x="Year",
    y="ActualHeadcount",
    markers=True,
    title="Enrolment Trends"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    """
    Strategic Insight:
    Rapid enrolment growth without proportional graduate growth
    may indicate declining throughput efficiency and increasing
    institutional sustainability risk.
    """
)

# ---------------------------------------------------
# GRADUATE TRENDS
# ---------------------------------------------------

graduate_trend = (
    df.groupby("Year")["Graduates"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    graduate_trend,
    x="Year",
    y="Graduates",
    title="Graduate Output Trends"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# SUCCESS RATE ANALYSIS
# ---------------------------------------------------

success_faculty = (
    df.groupby("Faculty")["SuccessRate"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    success_faculty,
    x="Faculty",
    y="SuccessRate",
    title="Average Success Rate by Faculty"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# RESEARCH OUTPUT ANALYSIS
# ---------------------------------------------------

research_trend = (
    df.groupby("Year")["ResearchOutputUnits"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    research_trend,
    x="Year",
    y="ResearchOutputUnits",
    markers=True,
    title="Research Output Trends"
)

st.plotly_chart(fig4, use_container_width=True)

st.warning(
    """
    Strategic Risk:
    Declining research outputs and postgraduate activity may weaken
    future DHET research subsidy generation and institutional competitiveness.
    """
)

# ---------------------------------------------------
# STRATEGIC & FUNDING RISKS
# ---------------------------------------------------

st.header("Strategic and Funding Risk Analysis")

# DHET Planning Variance
actual_total = df["ActualHeadcount"].sum()
approved_total = df["ApprovedPlanHeadcount"].sum()

variance = actual_total - approved_total

st.subheader("DHET Enrolment Planning Variance")

st.write(f"Actual Enrolments: {int(actual_total)}")
st.write(f"Approved Plan Enrolments: {int(approved_total)}")
st.write(f"Variance: {int(variance)}")

if variance > 0:
    st.error(
        """
        Enrolments exceed approved planning targets.
        Potential DHET compliance and infrastructure risk identified.
        """
    )

# Subsidy Efficiency
graduate_efficiency = (
    df["Graduates"].sum() /
    df["ActualHeadcount"].sum()
)

st.subheader("Graduate Efficiency Ratio")

st.write(
    f"Graduate Efficiency Ratio: {round(graduate_efficiency, 4)}"
)

st.info(
    """
    Lower graduate efficiency may indicate declining subsidy efficiency,
    weak throughput, and growing institutional cost pressures.
    """
)

# Capacity Utilisation
capacity_utilisation = (
    df["ActualHeadcount"].sum() /
    df["CapacitySeats"].sum()
) * 100

st.subheader("Infrastructure Capacity Utilisation")

st.write(
    f"Capacity Utilisation: {round(capacity_utilisation, 2)}%"
)

if capacity_utilisation > 100:
    st.error(
        """
        Institutional capacity exceeded.
        Infrastructure strain and overcrowding risks identified.
        """
    )

# ---------------------------------------------------
# DATA GOVERNANCE MODULE
# ---------------------------------------------------

st.header("Data Governance Module")

st.subheader("Missing Values")

st.write(df.isnull().sum())

st.subheader("Duplicate Records")

st.write(df.duplicated().sum())

# Validation Rule
if df["SuccessRate"].max() > 100:
    st.error("Invalid success rate detected.")

if df["DropoutRate"].min() < 0:
    st.error("Invalid dropout rate detected.")

st.success(
    """
    Data governance controls improve reporting integrity,
    decision-making quality, and institutional accountability.
    """
)

# ---------------------------------------------------
# PREDICTIVE ANALYTICS
# ---------------------------------------------------

st.header("Predictive Analytics")

forecast_df = (
    df.groupby("Year")["Graduates"]
    .sum()
    .reset_index()
)

X = forecast_df[["Year"]]
y = forecast_df["Graduates"]

model = LinearRegression()
model.fit(X, y)

future_years = np.array([[2025], [2026], [2027]])

predictions = model.predict(future_years)

forecast_results = pd.DataFrame({
    "Year": [2025, 2026, 2027],
    "Forecast Graduates": predictions.astype(int)
})

st.subheader("Graduate Forecast")

st.write(forecast_results)

fig5 = px.line(
    forecast_results,
    x="Year",
    y="Forecast Graduates",
    markers=True,
    title="Forecast Graduate Outputs"
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    """
    Forecasting enables proactive institutional planning,
    subsidy modelling, staffing alignment, and sustainability management.
    """
)

# ---------------------------------------------------
# EXECUTIVE CONCLUSION
# ---------------------------------------------------

st.header("Executive Institutional Insights")

st.write(
    """
    Key Institutional Findings:
    
    • Enrolment growth trends should be monitored alongside graduate productivity.
    
    • Throughput efficiency remains critical for subsidy sustainability.
    
    • Declining research outputs may weaken long-term institutional competitiveness.
    
    • Capacity pressures and over-enrolment may create DHET compliance risks.
    
    • Predictive analytics strengthens evidence-based planning and strategic decision-making.
    """
)
