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