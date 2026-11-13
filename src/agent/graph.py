
from src.agent.state import AgentState
from src.agent.router import route_question


def run_agent(user_question: str) -> AgentState:
    """
    Run the InsightX Agent workflow using plain Python.
    """

    # Step 1: Validate the user's question
    if not user_question or not user_question.strip():
        raise ValueError("Please enter a valid question.")

    # Remove unnecessary spaces
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

    # Step 4: Generate a temporary response
    state["tool_result"] = None

    state["final_answer"] = (
        f"Your question was routed to: {selected_tool}"
    )

    # Step 5: Return the updated state
    return state
