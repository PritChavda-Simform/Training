import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from utils_function.model_llm import llm 
from tools_function.music_agent_tools import mood_to_genre, fetch_playlist, fetch_song
from tools_function.human_feedback_tool import human_feedback
from logger_config.logger_config import logger

# Load environment variables
load_dotenv()

# Tools used by the music agent
tools = [mood_to_genre, fetch_song, fetch_playlist, human_feedback]

# ---------------------
# Music Chat Agent Function
# ---------------------
def music_run_chat(messages, feedback):
    try:
        logger.info("Starting music_run_chat function")

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
        logger.info("Creating ReAct agent for music tools")
        llm_search_agent = create_react_agent(model=llm, tools=tools, name="You are llm expert")

        logger.info("Invoking music agent with prompt")
        result = llm_search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        logger.info("Agent invocation complete")
        final_message = result['messages'][-1]
        logger.info("Final message returned by music agent: %s", final_message)

        return final_message

    except Exception as e:
        logger.exception("Exception occurred in music_run_chat: %s", e)
        raise
