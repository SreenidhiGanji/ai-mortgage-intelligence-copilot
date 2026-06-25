import pandas as pd
from langchain_core.documents import Document


def safe_value(value):
    if pd.isna(value):
        return "Not available"
    return value


def build_mortgage_documents(df: pd.DataFrame, limit: int = 500) -> list[Document]:
    """
    Converts HMDA rows into LangChain Document objects for RAG.
    Each document contains business-readable text and searchable metadata.
    """
    documents = []

    sample_df = df.head(limit)

    for index, row in sample_df.iterrows():
        state = safe_value(row.get("state_code"))
        county = safe_value(row.get("county_code"))
        loan_type = safe_value(row.get("loan_type_label"))
        loan_purpose = safe_value(row.get("loan_purpose_label"))
        action_taken = safe_value(row.get("action_taken_label"))
        loan_amount = safe_value(row.get("loan_amount"))
        income = safe_value(row.get("income"))
        property_value = safe_value(row.get("property_value"))
        interest_rate = safe_value(row.get("interest_rate"))
        occupancy_type = safe_value(row.get("occupancy_type"))

        page_content = f"""
Mortgage Application Summary:

A mortgage application was submitted in state {state}.

The applicant requested a {loan_type} loan for {loan_purpose}.

The reported action taken was: {action_taken}.

The loan amount was {loan_amount}.

The applicant income was {income}.

The property value was {property_value}.

The interest rate was {interest_rate}.

The occupancy type was {occupancy_type}.
"""

        metadata = {
            "record_id": str(index),
            "state": str(state),
            "county": str(county),
            "loan_type": str(loan_type),
            "loan_purpose": str(loan_purpose),
            "action_taken": str(action_taken)
        }

        documents.append(
            Document(
                page_content=page_content.strip(),
                metadata=metadata
            )
        )

    return documents