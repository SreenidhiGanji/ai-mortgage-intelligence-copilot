def executive_summary_prompt(metrics: dict) -> str:
    return f"""
You are a senior mortgage business analyst.

Create a concise executive summary based on the following HMDA mortgage metrics.

Metrics:
- Total Applications: {metrics["total_records"]}
- Approved Loans: {metrics["approved_count"]}
- Denied Loans: {metrics["denied_count"]}
- Denial Rate: {metrics["denial_rate"]}%
- Average Loan Amount: ${metrics["average_loan_amount"]:,.2f}

Write the summary in 4 bullet points:
1. Overall lending activity
2. Approval and denial performance
3. Loan amount insight
4. Business risk or opportunity
"""