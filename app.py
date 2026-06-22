import streamlit as st
import pandas as pd

from src.analytics import calculate_basic_metrics, get_top_values, filter_dataframe
from src.data_processor import load_csv, clean_hmda_data, add_business_labels

st.set_page_config(
    page_title="AI Mortgage Intelligence Copilot",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Mortgage Intelligence Copilot")
st.write("Upload HMDA mortgage data and discover lending insights.")

uploaded_file = st.file_uploader(
    "Upload HMDA CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    raw_df = load_csv(uploaded_file)
    df = clean_hmda_data(raw_df)
    df = add_business_labels(df)

    st.sidebar.header("Filters")

    state_options = ["All"] + sorted(df["state_code"].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("State", state_options)

    loan_type_options = ["All"] + sorted(df["loan_type_label"].dropna().unique().tolist())
    selected_loan_type = st.sidebar.selectbox("Loan Type", loan_type_options)

    action_options = ["All"] + sorted(df["action_taken_label"].dropna().unique().tolist())
    selected_action = st.sidebar.selectbox("Action Taken", action_options)

    loan_purpose_options = ["All"] + sorted(df["loan_purpose_label"].dropna().unique().tolist())
    selected_loan_purpose = st.sidebar.selectbox("Loan Purpose", loan_purpose_options)

    filtered_df = filter_dataframe(
        df,
        selected_state,
        selected_loan_type,
        selected_action,
        selected_loan_purpose
)

    st.success("CSV uploaded successfully!")
    st.info("Data cleaned successfully: column names standardized, numeric fields converted, and duplicate records removed.")

    st.write(f"Showing {len(filtered_df):,} records after applying filters.")

    metrics = calculate_basic_metrics(filtered_df)

    st.subheader("Mortgage Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Applications", metrics["total_records"])
    col2.metric("Approved Loans", metrics["approved_count"])
    col3.metric("Denied Loans", metrics["denied_count"])
    col4.metric("Denial Rate", f'{metrics["denial_rate"]}%')

    st.metric("Average Loan Amount", f'${metrics["average_loan_amount"]:,.2f}')

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head())

    st.subheader("Top States")
    top_states = get_top_values(filtered_df, "state_code")
    if top_states is not None:
        st.bar_chart(top_states)
    else:
        st.warning("state_code column not found.")

    st.subheader("Loan Type Distribution")
    loan_types = get_top_values(df, "loan_type_label")
    if loan_types is not None:
        st.bar_chart(loan_types)
    else:
        st.warning("loan_type column not found.")

    st.subheader("Action Taken Distribution")
    actions = get_top_values(df, "action_taken_label")
    if actions is not None:
        st.bar_chart(actions)
    else:
        st.warning("action_taken column not found.")

    st.subheader("Column Names")
    st.write(list(df.columns))

else:
    st.info("Please upload a HMDA CSV file to begin.")