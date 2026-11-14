
from src.database.query_executor import execute_read_only_query


# Predefined SQL queries supported by the agent
SQL_QUERIES = {
    "total_revenue": """
        SELECT SUM(revenue) AS total_revenue
        FROM sales
    """,

    "total_sales": """
        SELECT COUNT(*) AS total_records
        FROM sales
    """,

    "revenue_by_region": """
        SELECT region, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """
}


def run_sql_tool(query_type: str):
    """
    Execute a predefined business analytics query.
    """

    # Check whether the requested query is supported
    if query_type not in SQL_QUERIES:
        raise ValueError(
            f"Unsupported query type: {query_type}"
        )

    # Retrieve the corresponding SQL query
    sql_query = SQL_QUERIES[query_type]

    # Execute it using the restricted SQL executor
    result = execute_read_only_query(sql_query)

    return result
