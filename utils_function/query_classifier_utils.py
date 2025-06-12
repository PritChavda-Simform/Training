
from state_schema.states import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command,interrupt
from utils_function.model_llm import llm 

def question_classifier(state: AgentState) -> AgentState:
    print(state["messages"][-1].content)
    query = state["messages"][-1].content
    msg = [
        SystemMessage(content="In this project you have 4 agents: 1. movie_agent 2. music_agent 3. recipy_agent 4. genral_agent. Based on the following query, tell me which agent should be used. Just return one word: movie_agent, music_agent, recipy_agent, or genral_agent."),
        HumanMessage(content=query)
    ]
    result = llm(msg).content.strip().lower()
    print("The result is:", result)
    state["query_type"] = result
    return state  

def route_decision(state: AgentState) -> str:
    return state["query_type"] 

# def human_node(state:AgentState):
#     """Human Interavention node - loop back to model unless input is done"""
#     messages = state["messages"]
#     # print(messages)

#     print("Enter in human in the loop-----------------------------------------", state["query_type"])
#     user_feedback = interrupt(
#         {
#             "messages": messages,
#             "message" : "Provide feedback or type 'done' to finish"
#         }
#     )
#     print("human node recive feedback :",{user_feedback})

#     if user_feedback.lower() == "done":
#         return Command(update={"human_feedback": state["human_feedback"] + ["Finalised"]}, goto= END)
    
#     return Command(update={"human_feedback": state["human_feedback"] + [user_feedback]}, goto= state["query_type"])
