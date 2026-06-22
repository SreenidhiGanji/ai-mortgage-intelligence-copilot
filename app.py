import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Mortgage Intelligence Copilot",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Mortgage Intelligence Copilot")

st.write(
    "Upload HMDA mortgage data and discover lending insights."
)

uploaded_file = st.file_uploader(
    "Upload HMDA CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("CSV uploaded successfully!")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("Column Names")
    st.write(list(df.columns))

else:
    st.info("Please upload a HMDA CSV file to begin.")