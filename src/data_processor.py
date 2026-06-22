import pandas as pd

def load_csv(uploaded_file) -> pd.DataFrame:
    """
    Reads uploaded CSV file and returns a Pandas DataFrame.
    """
    return pd.read_csv(uploaded_file)


def clean_hmda_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans HMDA mortgage data for analytics.
    """
    cleaned_df = df.copy()

    cleaned_df.columns = (
        cleaned_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    numeric_columns = [
        "loan_amount",
        "income",
        "property_value",
        "interest_rate",
        "action_taken",
        "loan_type",
        "loan_purpose"
    ]

    for column in numeric_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )

    cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df

def add_business_labels(df: pd.DataFrame) -> pd.DataFrame:
    labeled_df = df.copy()

    action_taken_map = {
        1: "Loan originated",
        2: "Application approved but not accepted",
        3: "Application denied",
        4: "Application withdrawn",
        5: "File closed for incompleteness",
        6: "Purchased loan",
        7: "Preapproval denied",
        8: "Preapproval approved but not accepted"
    }

    loan_type_map = {
        1: "Conventional",
        2: "FHA",
        3: "VA",
        4: "USDA/RHS"
    }

    loan_purpose_map = {
        1: "Home purchase",
        2: "Home improvement",
        31: "Refinance",
        32: "Cash-out refinance"
    }

    if "action_taken" in labeled_df.columns:
        labeled_df["action_taken_label"] = labeled_df["action_taken"].map(action_taken_map)

    if "loan_type" in labeled_df.columns:
        labeled_df["loan_type_label"] = labeled_df["loan_type"].map(loan_type_map)

    if "loan_purpose" in labeled_df.columns:
        labeled_df["loan_purpose_label"] = labeled_df["loan_purpose"].map(loan_purpose_map)

    return labeled_df