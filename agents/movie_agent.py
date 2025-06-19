import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from utils_function.model_llm import llm 
# from tools_function.movie_agent_tools import movie_info, movie_playlist, movie_recommender
from logger_config.logger_config import logger
from tools_function.movie_agent_tools import MovieInfoTool, MoviePlaylistTool, MovieRecommenderTool
# from tools_function.human_feedback_tool import human_feedback
from tools_function.human_feedback_tool import HumanFeedbackTool




# Load environment variables
load_dotenv()

# Tools used by the agent
# tools = [movie_info, movie_playlist, movie_recommender, human_feedback]
tools = [MovieInfoTool(), MoviePlaylistTool(), MovieRecommenderTool(), HumanFeedbackTool()]
# ---------------------
# Movie Chat Agent Function
# ---------------------
def movie_run_chat(messages, feedback):
    try:
        logger.info("Starting movie_run_chat function")

        # Convert message objects to readable text
        history_texts = [
            f"Human: {m.content}" if isinstance(m, HumanMessage) else f"AI: {m.content}"
            for m in messages[-5:]
        ]
        user_query = messages[-1].content if messages else ""
        last_feedback = feedback[-1] if feedback else "No feedback yet"

        # Build prompt
        prompt = f"""You are provided from complete message history use it for user response
        you have an alos tool for fach a music TOol like fetch_songs so fach a songs from there 
        Human Feedback: {last_feedback}
        User Query: {user_query}
        History:
        {chr(10).join(history_texts)}
        Consider previous human feedback to refine the response.
        If the user’s question is incomplete or ambiguous, always call the human_feedback tool to request more information before answering."""

        logger.debug("Constructed prompt: %s", prompt)

        # Create and invoke the agent
        logger.info("Creating ReAct agent for movie tools")
        llm_search_agent = create_react_agent(model=llm, tools=tools, name="You are llm expert")

        logger.info("Invoking agent with prompt")
        result = llm_search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        logger.info("Agent invocation complete")
        logger.debug("Agent response: %s", result)

        final_message = result['messages'][-1]
        logger.info("Final message returned by movie agent: %s", final_message)

        return final_message

    except Exception as e:
        logger.exception("Exception occurred in movie_run_chat: %s", e)
        raise
