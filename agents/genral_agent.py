from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from utils_function.model_llm import llm 
# from tools_function.general_agent_tools import general_AI
from tools_function.general_agent_tools import GeneralAITool
# from tools_function.human_feedback_tool import human_feedback
from tools_function.human_feedback_tool import HumanFeedbackTool
from logger_config.logger_config import logger
# Load environment variables
load_dotenv()

# ---------------------
# Main Agent Function
# ---------------------

tools = [GeneralAITool(),HumanFeedbackTool()]

def genral_run_chat(message, feedback):
    try:
        logger.info("Creating ReAct agent with tools: general_AI, human_feedback")
        llm_search_agent = create_react_agent(
            model=llm, 
            tools=tools, 
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

        # logger.info("Agent invocation complete. Result: %s", result)
        # return result
    
        logger.info("Agent invocation complete")
        logger.debug("Agent response: %s", result)

        final_message = result['messages'][-1]
        logger.info("Final message returned by genral agent: %s", final_message)

        return final_message

    except Exception as e:
        logger.exception("in genral_run_chat")
        raise
                          