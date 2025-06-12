from langchain_core.tools import tool
from dummy_data.recipy_agent_dummy_data import taste_dishes
from utils_function.model_llm import llm
# ---- Tool Definition ----


@tool 
def recipy_Generator(name_dish):
    """
        Generates a cooking recipe based on the name of a dish. It uses an LLM (Large Language Model) to provide a detailed and dynamic recipe.
    """
    result = llm.invoke(f"give me an reciepy of {name_dish}")
    return result

@tool 
def fetch_deshname(message:str) -> str:
    """
        Suggests a dish based on a given taste or flavor preference. It maps taste descriptions (e.g., "spicy", "sweet") to relevant dishes. 
    """
    dishes = taste_dishes.get(message,["No dishes found."])
    return f"Here's your {dishes}"
