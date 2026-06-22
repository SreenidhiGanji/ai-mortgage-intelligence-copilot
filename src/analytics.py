import pandas as pd


def calculate_basic_metrics(df: pd.DataFrame) -> dict:
    total_records = len(df)

    approved_count = 0
    denied_count = 0
    denial_rate = 0

    if "action_taken" in df.columns:
        approved_count = len(df[df["action_taken"] == 1])
        denied_count = len(df[df["action_taken"] == 3])

        if total_records > 0:
            denial_rate = round((denied_count / total_records) * 100, 2)

    average_loan_amount = 0

    if "loan_amount" in df.columns:
        average_loan_amount = round(df["loan_amount"].mean(), 2)

    return {
        "total_records": total_records,
        "approved_count": approved_count,
        "denied_count": denied_count,
        "denial_rate": denial_rate,
        "average_loan_amount": average_loan_amount,
    }


def get_top_values(df: pd.DataFrame, column_name: str, limit: int = 10):
    if column_name not in df.columns:
        return None

    return df[column_name].value_counts().head(limit)