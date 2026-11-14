
from src.agent.state import AgentState
from src.agent.router import route_question
from src.tools.sql_tool import run_sql_tool


def identify_sql_query(user_question: str):
    """
    Identify which predefined SQL query matches the question.
    """

    question = user_question.lower()

    # Reject unsupported average calculations
    if "average" in question or "avg" in question:
        return None

    # Check for revenue grouped by region
    if (
        "by region" in question
        or "region-wise" in question
        or "region wise" in question
    ):
        return "revenue_by_region"

    # Check for the number of sales records
    sales_count_phrases = [
        "how many sales",
        "number of sales",
        "count sales",
        "sales count",
        "total sales"
    ]

    if any(phrase in question for phrase in sales_count_phrases):
        return "total_sales"

    # Check for explicitly requested total revenue
    total_revenue_phrases = [
        "total revenue",
        "overall revenue",
        "revenue generated",
        "sum of revenue",
        "sum revenue"
    ]

    if any(phrase in question for phrase in total_revenue_phrases):
        return "total_revenue"

    return None


def format_sql_result(query_type: str, result: list) -> str:
    """
    Convert SQL results into a readable response.
    """

    if query_type == "total_revenue":
        revenue = result[0]["total_revenue"]
        return f"The total revenue is ₹{revenue:,.2f}."

    if query_type == "total_sales":
        total_records = result[0]["total_records"]
        return f"The database contains {total_records} sales records."

    if query_type == "revenue_by_region":
        lines = ["Revenue by region:"]

        for record in result:
            region = record["region"]
            revenue = record["total_revenue"]

            lines.append(
                f"{region}: ₹{revenue:,.2f}"
            )

        return "\n".join(lines)

    return "The requested SQL operation is not supported yet."


def run_agent(user_question: str) -> AgentState:
    """
    Run the InsightX Agent workflow using plain Python.
    """

    # Step 1: Validate the user's question
    if not user_question or not user_question.strip():
        raise ValueError("Please enter a valid question.")

    user_question = user_question.strip()

    # Step 2: Create the initial agent state
    state: AgentState = {
        "user_question": user_question,
        "selected_tool": None,
        "tool_result": None,
        "final_answer": None
    }

    # Step 3: Identify the appropriate tool
    selected_tool = route_question(user_question)
    state["selected_tool"] = selected_tool

    # Step 4: Execute the SQL tool when selected
    if selected_tool == "sql":

        query_type = identify_sql_query(user_question)

        if query_type is None:
            state["final_answer"] = (
                "This SQL operation is not supported yet. "
                "Currently, I can answer questions about "
                "total revenue, total sales records, "
                "and revenue by region."
            )

        else:
            result = run_sql_tool(query_type)
            state["tool_result"] = result

            state["final_answer"] = format_sql_result(
                query_type,
                result
            )

    # Step 5: Keep other tool types unchanged
    else:
        state["final_answer"] = (
            f"Your question was routed to: {selected_tool}"
        )

    return state
