import pandas as pd


def build_mortgage_documents(df: pd.DataFrame, limit: int = 500) -> list[str]:
    """
    Converts HMDA rows into business-readable text documents for RAG.
    """
    documents = []

    sample_df = df.head(limit)

    for _, row in sample_df.iterrows():
        document = f"""
Mortgage Application Record:
State: {row.get("state_code", "Unknown")}
County: {row.get("county_code", "Unknown")}
Loan Type: {row.get("loan_type_label", "Unknown")}
Loan Purpose: {row.get("loan_purpose_label", "Unknown")}
Action Taken: {row.get("action_taken_label", "Unknown")}
Loan Amount: {row.get("loan_amount", "Unknown")}
Applicant Income: {row.get("income", "Unknown")}
Property Value: {row.get("property_value", "Unknown")}
Interest Rate: {row.get("interest_rate", "Unknown")}
Occupancy Type: {row.get("occupancy_type", "Unknown")}
"""
        documents.append(document.strip())

    return documents