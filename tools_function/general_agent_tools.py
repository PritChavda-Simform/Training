from langchain_core.tools import tool
from langchain_groq import ChatGroq
@tool
def general_AI(message: str) -> str:

    """Handles general queries asked by the user"""
    print("-------------------------------------")
    print("Entering in General ai")
    llmm = ChatGroq(model="llama-3.1-8b-instant")
    result = llmm.invoke(message)
    print("-------------------------------------")
    print("retutningh from genetal ai")
    return result
