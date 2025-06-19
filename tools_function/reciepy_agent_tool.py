from langchain_core.tools import tool
from dummy_data.recipy_agent_dummy_data import taste_dishes
from utils_function.model_llm import llm
from typing import List
from langchain_core.tools import BaseTool

class RecipyGeneratorTool(BaseTool):
    name: str = "recipy_Generator"
    description: str = (
        "Generates a cooking recipe based on the name of a dish using an LLM. "
        "Input should be a string like 'Pasta' or 'Butter Chicken'."
    )

    def _run(self, name_dish: str) -> str:
        return llm.invoke(f"Give me a recipe for {name_dish}")


class FetchDishNameTool(BaseTool):
    name: str = "fetch_deshname"
    description: str = (
        "Suggests dishes based on a given taste or flavor preference "
        "(e.g., spicy, sweet, sour). Input should be a taste keyword."
    )

    def _run(self, message: str) -> str:
        dishes = taste_dishes.get(message.lower(), ["No dishes found."])
        return f"Here are some dishes: {', '.join(dishes)}"


# @tool 
# def recipy_Generator(name_dish):
#     """
#         Generates a cooking recipe based on the name of a dish. It uses an LLM (Large Language Model) to provide a detailed and dynamic recipe.
#     """
#     result = llm.invoke(f"give me an reciepy of {name_dish}")
#     return result

# @tool 
# def fetch_deshname(message:str) -> str:
#     """
#         Suggests a dish based on a given taste or flavor preference. It maps taste descriptions (e.g., "spicy", "sweet") to relevant dishes. 
#     """
#     dishes = taste_dishes.get(message,["No dishes found."])
#     return f"Here's your {dishes}"
