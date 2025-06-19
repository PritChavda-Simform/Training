from state_schema.states import AgentState
from agents.music_agent import music_run_chat
from agents.recipy_agent import recipy_run_chat
from agents.genral_agent import genral_run_chat
from agents.movie_agent import movie_run_chat
from logger_config.logger_config import logger
# ---------------------
# Agent Wrappers
# ---------------------

def movie_agent(state: AgentState) -> AgentState:
    try:
        logger.info("Calling movie agent with state: %s", state)
        result = movie_run_chat(state["messages"], state["human_feedback"])
        logger.info("Movie agent result: %s", result)
        return {"messages": [result]}
    except Exception as e:
        logger.exception("Exception in movie_agent: %s", e)
        raise

def music_agent(state: AgentState) -> AgentState:
    try:
        logger.info("Calling music agent with state: %s", state)
        result = music_run_chat(state["messages"], state["human_feedback"])
        logger.info("Music agent result: %s", result)
        return {"messages": [result]}
    except Exception as e:
        logger.exception("Exception in music_agent: %s", e)
        raise

def recipy_agent(state: AgentState) -> AgentState:
    try:
        logger.info("Calling recipe agent with state: %s", state)
        result = recipy_run_chat(state["messages"], state["human_feedback"])
        logger.info("Recipe agent result: %s", result)
        return {"messages": [result]}
    except Exception as e:
        logger.exception("Exception in recipy_agent: %s", e)
        raise

def genral_agent(state: AgentState) -> AgentState:
    try:
        logger.info("Calling general agent with state: %s", state)
        result = genral_run_chat(state["messages"], state["human_feedback"])
        logger.info("General agent final message: %s", result)
        return {"messages": [result]}
    except Exception as e:
        logger.exception("Exception in genral_agent: %s", e)
        raise





