import streamlit as st
import pandas as pd

from src.analytics import (
    calculate_basic_metrics,
    get_top_values,
    filter_dataframe,
    get_chart_data
)

from src.data_processor import (
    load_csv,
    clean_hmda_data,
    add_business_labels
)

from src.ai_service import generate_executive_summary
from src.document_builder import build_mortgage_documents
from src.chunking_service import split_documents
from src.embedding_service import generate_embedding_for_text

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

    # Load and clean data
    raw_df = load_csv(uploaded_file)
    df = clean_hmda_data(raw_df)
    df = add_business_labels(df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    state_options = ["All"] + sorted(
        df["state_code"].dropna().unique().tolist()
    )

    selected_state = st.sidebar.selectbox(
        "State",
        state_options
    )

    loan_type_options = ["All"] + sorted(
        df["loan_type_label"].dropna().unique().tolist()
    )

    selected_loan_type = st.sidebar.selectbox(
        "Loan Type",
        loan_type_options
    )

    action_options = ["All"] + sorted(
        df["action_taken_label"].dropna().unique().tolist()
    )

    selected_action = st.sidebar.selectbox(
        "Action Taken",
        action_options
    )

    loan_purpose_options = ["All"] + sorted(
        df["loan_purpose_label"].dropna().unique().tolist()
    )

    selected_loan_purpose = st.sidebar.selectbox(
        "Loan Purpose",
        loan_purpose_options
    )

    # Apply Filters
    filtered_df = filter_dataframe(
        df,
        selected_state,
        selected_loan_type,
        selected_action,
        selected_loan_purpose
    )

    st.success("CSV uploaded successfully!")

    st.info(
        "Data cleaned successfully: column names standardized, "
        "numeric fields converted, and duplicate records removed."
    )

    st.write(
        f"Showing {len(filtered_df):,} records after applying filters."
    )

    documents = build_mortgage_documents(filtered_df, limit=100)
    chunks = split_documents(documents)

    # Metrics
    metrics = calculate_basic_metrics(filtered_df)

    st.subheader("Key Mortgage Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Applications",
        metrics["total_records"]
    )

    col2.metric(
        "Approved Loans",
        metrics["approved_count"]
    )

    col3.metric(
        "Denied Loans",
        metrics["denied_count"]
    )

    col4.metric(
        "Denial Rate",
        f'{metrics["denial_rate"]}%'
    )

    st.metric(
        "Average Loan Amount",
        f'${metrics["average_loan_amount"]:,.2f}'
    )

    # Visual Analytics
    st.subheader("Mortgage Visual Insights")

    # Loan Type Chart
    loan_chart = get_chart_data(
        filtered_df,
        "loan_type_label"
    )

    if loan_chart is not None:
        st.write("### Loan Type Distribution")
        st.bar_chart(
            loan_chart.set_index("loan_type_label")
        )

    # Action Taken Chart
    action_chart = get_chart_data(
        filtered_df,
        "action_taken_label"
    )

    if action_chart is not None:
        st.write("### Action Taken Distribution")
        st.bar_chart(
            action_chart.set_index("action_taken_label")
        )

    # Loan Purpose Chart
    purpose_chart = get_chart_data(
        filtered_df,
        "loan_purpose_label"
    )

    if purpose_chart is not None:
        st.write("### Loan Purpose Distribution")
        st.bar_chart(
            purpose_chart.set_index("loan_purpose_label")
        )

    # Top States
    st.subheader("Top States")

    top_states = get_top_values(
        filtered_df,
        "state_code"
    )

    if top_states is not None:
        st.bar_chart(top_states)
    else:
        st.warning("state_code column not found.")

    st.subheader("RAG Document Preview")

    if st.checkbox("Show generated mortgage documents"):
        st.write(f"Generated {len(documents)} mortgage documents for AI search.")
        st.write(f"Generated {len(chunks)} chunks for embeddings.")
        st.text(documents[0].page_content)
        st.write("Metadata:")
        st.json(documents[0].metadata)

    st.subheader("Embedding Test")

    if st.button("Generate Sample Embedding"):
        with st.spinner("Generating embedding..."):
            sample_embedding = generate_embedding_for_text(
                chunks[0].page_content
            )

            st.write(f"Embedding generated successfully.")
            st.write(f"Vector dimensions: {len(sample_embedding)}")
            st.write(sample_embedding[:10])

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head())

    # Dataset Schema
    st.subheader("Dataset Schema")
    st.write(list(df.columns))

    st.subheader("AI Executive Summary")

    if st.button("Generate AI Executive Summary"):
     with st.spinner("Generating executive summary..."):
         summary = generate_executive_summary(metrics)
         st.write(summary)

else:
    st.info(
        "Please upload a HMDA CSV file to begin."
    )