from langgraph.graph import StateGraph,START,END
from state_schema.states import AgentState
from dotenv import load_dotenv
from memory.mongo_memory import memory_checkpointer
from utils_function.routing_utils import movie_agent,music_agent,recipy_agent,genral_agent
from utils_function.query_classifier_utils import question_classifier,route_decision
from utils_function.routing_utils import movie_agent,music_agent,recipy_agent,genral_agent
load_dotenv()



graph = StateGraph(AgentState)
graph.add_node("movie_agent",movie_agent)
graph.add_node("music_agent",music_agent)
graph.add_node("recipy_agent",recipy_agent)
graph.add_node("genral_agent",genral_agent)
graph.add_node("question_classifier", question_classifier)
graph.add_node("router",lambda state:state)

graph.add_edge(START,"question_classifier")
graph.add_edge("question_classifier","router")
graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "movie_agent":"movie_agent",
        "music_agent":"music_agent",
        "recipy_agent":"recipy_agent",
        "genral_agent":"genral_agent",
    }
)




graph.add_edge("movie_agent",END)
graph.add_edge("music_agent",END)
graph.add_edge("recipy_agent",END)
graph.add_edge("genral_agent",END)

app = graph.compile(checkpointer=memory_checkpointer)



# graph.add_edge("movie_agent","userr_feedback")
# graph.add_edge("music_agent","userr_feedback")
# graph.add_edge("recipy_agent","userr_feedback")
# graph.add_edge("genral_agent","userr_feedback")
# graph.add_edge("userr_feedback", "end_nnode")
# graph.add_edge("end_nnode", END)



# checkpointer = MongoDBSaver.from_conn_string(MONGODB_URI, DB_NAME)
# with MongoDBSaver.from_conn_string(MONGODB_URI, DB_NAME) as checkpointer:
# ✅ Manually open MongoDBSaver
# checkpointer = MongoDBSaver.from_conn_string(MONGODB_URI, DB_NAME).__enter__()


# input_state = {
#     "messages": [HumanMessage(content="My mood is sad so recommend movie according to my mood")],
#     "human_feedback": []
# }
# thread_config = {"configurable": {"thread_id": "7"}}
# ress = app.invoke(input_state,config=thread_config)
# print("ress is ", ress)

# ---------------------------------------------------------------------------------------------------------

# st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
# st.title("🧠 LangGraph Chatbot (HITL Enabled)")
# thread_config = {"configurable": {"thread_id": "887"}}
# # Setup
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "human_feedback" not in st.session_state:
#     st.session_state.human_feedback = []
# if "phase" not in st.session_state:
#     st.session_state.phase = "ask_user"  # or "waiting_feedback", "processing_feedback"
# if "last_feedback" not in st.session_state:
#     st.session_state.last_feedback = None

# # Show chat history
# print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",st.session_state.messages )
# for msg in st.session_state.messages:
#     with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
#         print("The msg valus is ====================================================" , msg)
#         st.markdown(msg.content)
# # 1. Process feedback phase
# if st.session_state.phase == "processing_feedback":
#     print("**************************************************************, Processing Feedback feed baack is", st.session_state.last_feedback)
#     feedback = st.session_state.last_feedback
#     # if feedback.lower() == "done":
#     #     st.session_state.phase = "ask_user"
#     #     st.session_state.last_feedback = None
#     #     st.rerun()
#     # else:
#         # Send feedback to model
        
#     result = app.invoke(Command(resume=feedback), config=thread_config)

#     if "messages" in result:
#         ai_msg = result["messages"][-1]
#         st.session_state.messages.append(ai_msg)

#     st.session_state.phase = "ask_user"
#     st.session_state.last_feedback = None
#     st.rerun()

# # 2. Handle feedback input
# elif st.session_state.phase == "waiting_feedback":
#     print("********************************************************, Waiting_feedback")
#     feedback = st.chat_input("🔁 Provide feedback (or type 'done')")

#     if feedback:
#         st.session_state.human_feedback.append(feedback)
#         st.session_state.last_feedback = feedback
#         st.session_state.phase = "processing_feedback"
#         st.rerun()

# # 3. Handle initial user input
# elif prompt := st.chat_input("Ask something..."):
#     print("*********************************************************, Handle initial user input  ", st.session_state.phase)
#     mm_container = st.empty()
#     user_msg = HumanMessage(content=prompt)
#     mmm = st.session_state.messages
#     if mmm:
#         if mmm[-1].content != user_msg:
#             st.session_state.messages.append(user_msg)
#             # mm_container.markdown(user_msg)
#     else:
#             st.session_state.messages.append(user_msg)
#             # mm_container.markdown(user_msg)

#     input_state = {
#         "messages": st.session_state.messages,
#         "human_feedback": st.session_state.human_feedback
#     }
#     stream = app.stream(input_state, config=thread_config)

#     with st.chat_message("assistant"):
#         msg_container = st.empty()
#         for chunk in stream:
#             for node_id, value in chunk.items():
#                 if node_id == "__interrupt__":
#                     print("[VALUE_0]",type(value[0].value))
#                     print("[VALUE_0]",value[0].value)
#                     # ai_msg = value[0].value
#                     # print("value[0].value['messages'][-1]", ai_msg)
#                     # msg_container.markdown(ai_msg)
#                     msg_container.markdown(AIMessage(content=value[0].value))
#                     st.session_state.messages.append(AIMessage(content = value[0].value))
#                     st.session_state.phase = "waiting_feedback"
#                     st.rerun()
#                 elif "messages" in value:
#                     ai_msg = value["messages"][-1]
#                     msg_container.markdown(ai_msg.content)
#                     st.session_state.messages.append(ai_msg)




# st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
# st.title("🧠 LangGraph Chatbot (HITL Enabled)")

# # Initialize state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "human_feedback" not in st.session_state:
#     st.session_state.human_feedback = []
# if "awaiting_feedback" not in st.session_state:
#     st.session_state.awaiting_feedback = False
# if "last_ai_message" not in st.session_state:
#     st.session_state.last_ai_message = None

# # Show messages
# for msg in st.session_state.messages:
#     if isinstance(msg, HumanMessage):
#         with st.chat_message("user"):
#             st.markdown(msg.content)
#     elif isinstance(msg, AIMessage):
#         with st.chat_message("assistant"):
#             st.markdown(msg.content)

# # 1. Awaiting Feedback Phase
# if st.session_state.awaiting_feedback:
#     feedback = st.chat_input("🔁 Feedback (or type 'done')")
#     print("***************************************************************************", feedback)
#     if feedback:
#         st.session_state.human_feedback.append(feedback)
#         if feedback.lower() == "done":
#             st.session_state.awaiting_feedback = False
#             st.stop()
#         else:
#             # Simulate feedback-based continuation
#             thread_config = {"configurable": {"thread_id": "787"}}
#             app.invoke(Command(resume=feedback), config=thread_config)
#             st.session_state.awaiting_feedback = False
#             st.rerun()  # Go back to input mode

# # 2. User Asking a New Question
# elif prompt := st.chat_input("Ask something..."):
#     user_msg = HumanMessage(content=prompt)
#     st.session_state.messages.append(user_msg)
#     input_state = {
#         "messages": st.session_state.messages,
#         "human_feedback": st.session_state.human_feedback
#     }

#     thread_config = {"configurable": {"thread_id": "787"}}
#     stream = app.stream(input_state, config=thread_config)

#     with st.chat_message("assistant"):
#         msg_container = st.empty()

#         for chunk in stream:
#             for node_id, value in chunk.items():
#                 if node_id == "__interrupt__":
#                     ai_msg = value[0].value['messages'][-1]
#                     msg_container.markdown(ai_msg.content)
#                     st.session_state.last_ai_message = ai_msg
#                     st.session_state.messages.append(ai_msg)
#                     st.session_state.awaiting_feedback = True
#                     st.rerun()  # Rerun to trigger feedback input

#                 elif "messages" in value:
#                     ai_msg = value["messages"][-1]
#                     st.session_state.messages.append(ai_msg)
#                     msg_container.markdown(ai_msg.content)

    # print("-----------------------------------------------------------------------------------------------")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Goodbye!")
#         break

#     input_state = {
#         "messages": [HumanMessage(content=user_input)],
#         "human_feedback": []
#     }
    
#     thread_config = {"configurable": {"thread_id": "7"}}
    
#     # Run the app with streaming so we can handle interrupts
#     stream = app.stream(input_state, config=thread_config)
    
#     for chunk in stream:
#         for node_id, value in chunk.items():
#             # Handle human-in-the-loop interrupt
#             if node_id == "__interrupt__":
#                 while True:
#                     if "messages" in value:
#                         print("Final Result:")
#                         print(value["messages"][-1].content)
#                     user_feedback = input("Provide feedback (or type 'done' when finished): ")

#                     # Resume graph execution with user's feedback
#                     resume_result = app.invoke(Command(resume=user_feedback), config=thread_config)

#                     # If done, break out of feedback loop
#                     if user_feedback.lower() == "done":
#                         if "messages" in value:
#                             print("Final Result:")
#                             print(value["messages"][-1].content)
#                         break
#             else:
#                 # Final result should contain the updated messages
#                 if "messages" in value:
#                     print("Final Result:")
#                     print(value["messages"][-1].content)



#   st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
#     st.title("🧠 LangGraph Chatbot (HITL Enabled)")

#     # Initialize session state
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "human_feedback" not in st.session_state:
#         st.session_state.human_feedback = []

#     # Display previous messages
#     for msg in st.session_state.messages:
#         if isinstance(msg, HumanMessage):
#             with st.chat_message("user"):
#                 st.markdown(msg.content)
#         elif isinstance(msg, AIMessage):
#             with st.chat_message("assistant"):
#                 st.markdown(msg.content)

#     # Accept new input
#     if prompt := st.chat_input("Ask something..."):
#         user_msg = HumanMessage(content=prompt)
#         st.session_state.messages.append(user_msg)

#         input_state = {
#             "messages": st.session_state.messages,
#             "human_feedback": st.session_state.human_feedback
#         }
#         thread_config = {"configurable": {"thread_id": "175"}}

#         stream = app.stream(input_state, config=thread_config)
#         with st.chat_message("assistant"):
#             msg_container = st.empty()

#             for chunk in stream:
#                 for node_id, value in chunk.items():
#                     if node_id == "__interrupt__":
            
#                         # if "messages" in value:
#                         ai_msg = value[0]
#                         messagee = ai_msg.value['messages'][-1].content
#                         msg_container.markdown(messagee)

#                         # Ask for feedback using UI input
#                         feedback = st.chat_input("🔁 Feedback (or type 'done')", key="feedback_input")
#                         # if feedback := st.chat_input("🔁 Feedback (or type 'done')"):
#                         time.sleep(20)
#                         print("hellowwwwwwwwwwwwwwwwwwwwwwwwwww")
#                         a =0
#                         while True:
#                             a = a+1
#                             print(a)
#                             print("this is work --------------------------------------------------------------------********************", feedback)
#                             if feedback:
#                                 print("the feed back is =====", feedback)
#                                 break
#                             time.sleep(5)
#                         print("The feedback is this",feedback)
#                         if feedback:
#                             st.session_state.human_feedback.append(feedback)
#                             print("feed back is sending ..........")
#                             app.invoke(Command(resume=feedback), config=thread_config)
#                             print("feed back is stoping ..........")
#                             if feedback.lower() == "done":
#                                 break

#                     elif "messages" in value:

#                         print("It is running for final anser .......................................")
#                         ai_msg = value["messages"][-1]
#                         # msg_container.markdown(ai_msg.content)
#                         st.session_state.messages.append(ai_msg)
