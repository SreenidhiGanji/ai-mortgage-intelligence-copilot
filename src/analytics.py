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

def filter_dataframe(
    df: pd.DataFrame,
    state=None,
    loan_type=None,
    action_taken=None,
    loan_purpose=None
) -> pd.DataFrame:
    filtered_df = df.copy()

    if state and state != "All":
        filtered_df = filtered_df[filtered_df["state_code"] == state]

    if loan_type and loan_type != "All":
        filtered_df = filtered_df[filtered_df["loan_type_label"] == loan_type]

    if action_taken and action_taken != "All":
        filtered_df = filtered_df[filtered_df["action_taken_label"] == action_taken]

    if loan_purpose and loan_purpose != "All":
        filtered_df = filtered_df[filtered_df["loan_purpose_label"] == loan_purpose]

    return filtered_df

def generate_business_summary(metrics: dict) -> str:
    return (
        f"This dataset contains {metrics['total_records']:,} mortgage applications. "
        f"Out of these, {metrics['approved_count']:,} were originated and "
        f"{metrics['denied_count']:,} were denied. "
        f"The overall denial rate is {metrics['denial_rate']}%. "
        f"The average loan amount is ${metrics['average_loan_amount']:,.2f}. "
        "These metrics help identify lending performance, approval trends, and potential market risk."
    )