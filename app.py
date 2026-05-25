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
    governance, predictive analytics, and sustainability analysis.
    """
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_excel("Faculty Enrolment.xlsx")

# ---------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------

df["SuccessRate"] = df["SuccessRate"] * 100
df["DropoutRate"] = df["DropoutRate"] * 100

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

faculty_filter = st.sidebar.selectbox(
    "Select Faculty",
    ["All"] + sorted(df["Faculty"].unique())
)

year_filter = st.sidebar.multiselect(
    "Select Year(s)",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

if faculty_filter != "All":
    df = df[df["Faculty"] == faculty_filter]

df = df[df["Year"].isin(year_filter)]

# ---------------------------------------------------
# EXECUTIVE KPI SECTION
# ---------------------------------------------------

st.header("Executive Institutional Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Enrolments",
        f"{int(df['ActualHeadcount'].sum()):,}"
    )

with col2:
    st.metric(
        "Total Graduates",
        f"{int(df['Graduates'].sum()):,}"
    )

with col3:
    st.metric(
        "Average Success Rate",
        f"{round(df['SuccessRate'].mean(), 2)}%"
    )

with col4:
    st.metric(
        "Research Outputs",
        f"{round(df['ResearchOutputUnits'].sum(), 2):,}"
    )

with col5:
    st.metric(
        "Average Dropout Rate",
        f"{round(df['DropoutRate'].mean(), 2)}%"
    )

# ---------------------------------------------------
# INSTITUTIONAL PERFORMANCE ANALYTICS
# ---------------------------------------------------

st.header("Institutional Performance Analytics")

# ---------------------------------------------------
# ENROLMENT TRENDS
# ---------------------------------------------------

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
    title="Institutional Enrolment Trends"
)

fig1.update_layout(
    yaxis_tickformat=","
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    """
    Strategic Insight:
    Rapid enrolment growth without proportional graduate growth
    may indicate declining throughput efficiency and increasing
    institutional sustainability risks.
    """
)

# ---------------------------------------------------
# ENROLMENT MIX
# ---------------------------------------------------

if "QualificationType" in df.columns:

    st.subheader("Institutional Enrolment Mix")

    enrolment_mix = (
        df.groupby("QualificationType")["ActualHeadcount"]
        .sum()
        .reset_index()
    )

    fig_mix = px.pie(
        enrolment_mix,
        names="QualificationType",
        values="ActualHeadcount",
        title="Enrolment Distribution by Qualification Type"
    )

    st.plotly_chart(fig_mix, use_container_width=True)

else:

    st.warning(
        """
        QualificationType column not found in dataset.
        Enrolment mix analysis unavailable.
        """
    )

# ---------------------------------------------------
# QUALIFICATION ANALYSIS
# ---------------------------------------------------

if "QualificationType" in df.columns:

    st.header("Qualification Level Analysis")

    qualification_trend = (
        df.groupby(["Year", "QualificationType"])["ActualHeadcount"]
        .sum()
        .reset_index()
    )

    fig_qualification = px.bar(
        qualification_trend,
        x="Year",
        y="ActualHeadcount",
        color="QualificationType",
        barmode="group",
        title="Undergraduate vs Postgraduate Enrolment Trends"
    )

    fig_qualification.update_layout(
        yaxis_tickformat=","
    )

    st.plotly_chart(fig_qualification, use_container_width=True)

    st.info(
        """
        Qualification mix influences subsidy generation,
        postgraduate growth, and research sustainability.
        """
    )

else:

    st.warning(
        """
        QualificationType column not found in dataset.
        Qualification analysis unavailable.
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

fig2.update_layout(
    yaxis_tickformat=","
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

fig3.update_layout(
    yaxis_title="Success Rate (%)"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# FACULTY PERFORMANCE ANALYSIS
# ---------------------------------------------------

st.header("Faculty Performance Comparison")

faculty_summary = (
    df.groupby("Faculty")[
        ["Graduates", "ResearchOutputUnits", "ActualHeadcount"]
    ]
    .sum()
    .reset_index()
)

fig_faculty = px.bar(
    faculty_summary,
    x="Faculty",
    y=["Graduates", "ResearchOutputUnits"],
    barmode="group",
    title="Faculty Graduate and Research Performance"
)

fig_faculty.update_layout(
    yaxis_tickformat=","
)

st.plotly_chart(fig_faculty, use_container_width=True)

st.warning(
    """
    Faculties with declining graduate or research performance
    may require strategic intervention and resource support.
    """
)

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

fig4.update_layout(
    yaxis_tickformat=","
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

# ---------------------------------------------------
# DHET PLANNING VARIANCE
# ---------------------------------------------------

actual_total = df["ActualHeadcount"].sum()
approved_total = df["ApprovedPlanHeadcount"].sum()

variance = actual_total - approved_total

st.subheader("DHET Enrolment Planning Variance")

st.write(f"Actual Enrolments: {int(actual_total):,}")
st.write(f"Approved Plan Enrolments: {int(approved_total):,}")
st.write(f"Variance: {int(variance):,}")

if variance > 0:
    st.error(
        """
        Enrolments exceed approved planning targets.
        Potential DHET compliance and infrastructure risk identified.
        """
    )

# ---------------------------------------------------
# GRADUATE EFFICIENCY
# ---------------------------------------------------

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

# ---------------------------------------------------
# CAPACITY UTILISATION
# ---------------------------------------------------

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
# BENCHMARKING
# ---------------------------------------------------

st.header("Institutional Benchmarking")

national_success_rate = 78

institution_success_rate = round(
    df["SuccessRate"].mean(),
    2
)

st.write(
    f"Institution Success Rate: {institution_success_rate}%"
)

st.write(
    f"National Benchmark Success Rate: {national_success_rate}%"
)

if institution_success_rate < national_success_rate:
    st.warning(
        """
        Institutional success performance is below
        the national benchmark.
        """
    )
else:
    st.success(
        """
        Institutional success performance exceeds
        the national benchmark.
        """
    )

# ---------------------------------------------------
# DATA GOVERNANCE MODULE
# ---------------------------------------------------

st.header("Data Governance Module")

# ---------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------

st.subheader("Missing Values")

st.write(df.isnull().sum())

# ---------------------------------------------------
# DUPLICATES
# ---------------------------------------------------

st.subheader("Duplicate Records")

st.write(df.duplicated().sum())

# ---------------------------------------------------
# VALIDATION RULES
# ---------------------------------------------------

if df["SuccessRate"].max() > 100:
    st.error("Invalid success rate detected.")

if df["DropoutRate"].min() < 0:
    st.error("Invalid dropout rate detected.")

if (df["Graduates"] > df["ActualHeadcount"]).any():
    st.error(
        "Graduates cannot exceed enrolments."
    )

st.success(
    """
    Data governance controls improve reporting integrity,
    accountability, and institutional decision-making quality.
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

forecast_results["Lower Bound"] = (
    forecast_results["Forecast Graduates"] * 0.95
).astype(int)

forecast_results["Upper Bound"] = (
    forecast_results["Forecast Graduates"] * 1.05
).astype(int)

forecast_results["Year"] = (
    forecast_results["Year"].astype(int)
)

st.subheader("Graduate Forecast")

st.write(forecast_results)

fig5 = px.line(
    forecast_results,
    x="Year",
    y="Forecast Graduates",
    markers=True,
    title="Forecast Graduate Outputs"
)

fig5.add_scatter(
    x=forecast_results["Year"],
    y=forecast_results["Lower Bound"],
    mode='lines',
    name='Lower Forecast Bound'
)

fig5.add_scatter(
    x=forecast_results["Year"],
    y=forecast_results["Upper Bound"],
    mode='lines',
    name='Upper Forecast Bound'
)

fig5.update_layout(
    xaxis=dict(
        tickmode='linear'
    ),
    yaxis_tickformat=","
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    """
    Forecasting supports proactive institutional planning,
    sustainability analysis, staffing alignment,
    and strategic decision-making.
    """
)

# ---------------------------------------------------
# EXECUTIVE REPORT EXPORT
# ---------------------------------------------------

st.header("Executive Report Export")

executive_report = forecast_results.to_csv(index=False)

st.download_button(
    label="Download Forecast Report",
    data=executive_report,
    file_name="institutional_forecast_report.csv",
    mime="text/csv"
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

    • Qualification mix influences long-term research and funding sustainability.

    • Predictive analytics strengthens evidence-based planning and institutional decision-making.

    • Strong data governance improves reporting integrity and executive accountability.
    """
)
