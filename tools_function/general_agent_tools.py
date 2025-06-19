from langchain_core.tools import tool
from langchain_groq import ChatGroq

from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq

class GeneralAITool(BaseTool):
    name: str = "general_AI"
    description: str = "Handles general queries asked by the user."

    def _run(self, message: str) -> str:
                
        llmm = ChatGroq(model="llama-3.1-8b-instant")
        result = llmm.invoke(message)

        return result


# @tool
# def general_AI(message: str) -> str:

#     """Handles general queries asked by the user"""
#     print("-------------------------------------")
#     print("Entering in General ai")
#     llmm = ChatGroq(model="llama-3.1-8b-instant")
#     result = llmm.invoke(message)
#     print("-------------------------------------")
#     print("retutningh from genetal ai")
#     return result
