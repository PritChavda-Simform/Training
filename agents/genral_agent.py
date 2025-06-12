from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from utils_function.model_llm import llm 
from tools_function.general_agent_tools import general_AI
from tools_function.human_feedback_tool import human_feedback
from logger_config.logger_config import logger
# Load environment variables
load_dotenv()

# ---------------------
# Main Agent Function
# ---------------------
def genral_run_chat(message, feedback):
    try:
        logger.info("Creating ReAct agent with tools: general_AI, human_feedback")
        llm_search_agent = create_react_agent(
            model=llm, 
            tools=[general_AI, human_feedback], 
            name="You are llm expert"
        )

        logger.info("Entering llm search agent invocation")
        prompt = f"""You are provided from complete message history use it for user response
        Human Feedback: {feedback[-1] if feedback else "No feedback yet"}
        user query: {message[-1]}
        history : {message[-5:]}
        Consider previous human feedback to refine the response.
        If the user’s question is incomplete or ambiguous, always call the human_feedback tool to request more information before answering.
        """

        logger.debug("Prompt constructed: %s", prompt)

        result = llm_search_agent.invoke({"messages": [{
            "role": "user",
            "content": prompt
        }]})

        logger.info("Agent invocation complete. Result: %s", result)
        return result

    except Exception as e:
        logger.exception("Exception occurred in genral_run_chat: %s", e)
        raise
