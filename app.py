import streamlit as st
import pandas as pd

st.title("Institutional Analytics Dashboard")

st.write("Welcome to the dashboard")

df = pd.read_excel("Faculty Enrolment.xlsx")

st.write(df.head())
