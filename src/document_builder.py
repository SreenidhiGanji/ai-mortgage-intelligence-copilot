import pandas as pd


def safe_value(value):
    if pd.isna(value):
        return "Not available"
    return value


def build_mortgage_documents(df: pd.DataFrame, limit: int = 500) -> list[str]:
    """
    Converts HMDA rows into business-readable text documents for RAG.
    """
    documents = []

    sample_df = df.head(limit)

    for _, row in sample_df.iterrows():
        document = f"""
Mortgage Application Record:
State: {safe_value(row.get("state_code"))}
County: {safe_value(row.get("county_code"))}
Loan Type: {safe_value(row.get("loan_type_label"))}
Loan Purpose: {safe_value(row.get("loan_purpose_label"))}
Action Taken: {safe_value(row.get("action_taken_label"))}
Loan Amount: {safe_value(row.get("loan_amount"))}
Applicant Income: {safe_value(row.get("income"))}
Property Value: {safe_value(row.get("property_value"))}
Interest Rate: {safe_value(row.get("interest_rate"))}
Occupancy Type: {safe_value(row.get("occupancy_type"))}
"""
        documents.append(document.strip())

    return documents