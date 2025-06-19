import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from utils_function.model_llm import llm 
# from tools_function.reciepy_agent_tool import fetch_deshname, recipy_Generator
from tools_function.reciepy_agent_tool import RecipyGeneratorTool, FetchDishNameTool
# from tools_function.human_feedback_tool import human_feedback
from tools_function.human_feedback_tool import HumanFeedbackTool
from logger_config.logger_config import logger
# Load environment variables
load_dotenv()

# Tools used in this agent
# tools = [fetch_deshname, recipy_Generator, human_feedback]
tools = [
    RecipyGeneratorTool(),
    FetchDishNameTool(),
    HumanFeedbackTool()
]

# ---------------------
# Recipe Chat Agent Function
# ---------------------
def recipy_run_chat(messages, feedback):
    try:
        logger.info("Starting recipy_run_chat function")

        # Extract latest messages and feedback
        history_texts = [
            f"Human: {m.content}" if isinstance(m, HumanMessage) else f"AI: {m.content}"
            for m in messages[-5:]
        ]
        user_query = messages[-1].content if messages else ""
        last_feedback = feedback[-1] if feedback else "No feedback yet"

        # Construct the prompt
        prompt = f"""You are provided from complete message history use it for user response
        Human Feedback: {last_feedback}
        User Query: {user_query}
        History:
        {chr(10).join(history_texts)}
        Consider previous human feedback to refine the response.
        If the user’s question is incomplete or ambiguous, always call the human_feedback tool to request more information before answering."""

        logger.debug("Constructed prompt: %s", prompt)

        # Create and run the ReAct agent
        logger.info("Creating ReAct agent for recipe tools")
        llm_search_agent = create_react_agent(model=llm, tools=tools, name="You are llm expert")

        logger.info("Invoking recipe agent with prompt")
        result = llm_search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        final_message = result['messages'][-1]
        logger.info("Agent responded with message: %s", final_message)

        return final_message

    except Exception as e:
        logger.exception("Exception occurred in recipy_run_chat: %s", e)
        raise
