
def route_question(user_question: str) -> str:
    """
    Identify which tool should handle the user's question.
    """

    question = user_question.lower()

    # Check whether the user wants a chart
    chart_keywords = ["chart", "graph", "visualization", "trend"]

    if any(word in question for word in chart_keywords):
        return "sql_chart"

    # Check whether the user wants document information
    document_keywords = ["pdf", "document", "report", "uploaded file"]

    if any(word in question for word in document_keywords):
        return "rag"

    # Check whether the user wants structured data analysis
    sql_keywords = [
        "average", "total", "revenue", "sales",
        "highest", "lowest", "count", "sum"
    ]

    if any(word in question for word in sql_keywords):
        return "sql"

    # Default option when no rule matches
    return "answer"
