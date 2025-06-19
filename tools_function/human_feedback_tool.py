from langchain_core.tools import tool
from langchain_core.tools import BaseTool
from langgraph.types import interrupt

class HumanFeedbackTool(BaseTool):
    name: str = "human_feedback"
    description: str = (
        "Requests clarification or more details from the user for the given query. "
        "This tool is useful when the input is ambiguous or unclear."
    )

    def _run(self, message: str) -> str:
        print("\n[🔎 Awaiting human input for clarification...]\n")
        prompt = f"❓ Please clarify: {message}"

        # Triggers a human interrupt for clarification
        user_feedback = interrupt({prompt})

        print("[✅ Received human clarification]\n")
        return user_feedback


# @tool
# def human_feedback(message: str) -> str:
#     """
#     Requests clarification or more details from the user for the given query.
#     This function can be reused anytime clarity is needed across multiple agent steps.

#     Parameters:
#     - query (str): The ambiguous or unclear input/query.

#     Returns:
#     - str: User's feedback or clarification.
#     """
#     print("\n[🔎 Awaiting human input for clarification...]\n")

#     prompt = f"❓ Please clarify: {message}"

#     # interrupt() simulates waiting for external human input
#     user_feedback = interrupt({message})

#     print("[✅ Received human clarification]\n")
#     return user_feedback