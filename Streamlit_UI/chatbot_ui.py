import streamlit as st
from langgraph.types import Command,interrupt
from  work_flow.work_flow import app
from langchain_core.messages import HumanMessage,AIMessage

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🧠 LangGraph Chatbot (HITL Enabled)")
thread_config = {"configurable": {"thread_id": "7534"}}
# Setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "human_feedback" not in st.session_state:
    st.session_state.human_feedback = []
if "phase" not in st.session_state:
    st.session_state.phase = "ask_user"  # or "waiting_feedback", "processing_feedback"
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

# Show chat history

for msg in st.session_state.messages:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        print("The msg valus is ====================================================" , msg)
        st.markdown(msg.content)
# 1. Process feedback phase
if st.session_state.phase == "processing_feedback":
    feedback = st.session_state.last_feedback
    # if feedback.lower() == "done":
    #     st.session_state.phase = "ask_user"
    #     st.session_state.last_feedback = None
    #     st.rerun()
    # else:
        # Send feedback to model
        
    result = app.invoke(Command(resume=feedback), config=thread_config)

    if "messages" in result:
        ai_msg = result["messages"][-1]
        st.session_state.messages.append(ai_msg)
        
    st.session_state.phase = "ask_user"
    st.session_state.last_feedback = None
    st.rerun()

# 2. Handle feedback input
elif st.session_state.phase == "waiting_feedback":
   
    feedback = st.chat_input("🔁 Provide feedback (or type 'done')")

    if feedback:
        st.session_state.human_feedback.append(feedback)
        st.session_state.last_feedback = feedback
        st.session_state.phase = "processing_feedback"
        st.rerun()

# 3. Handle initial user input
elif prompt := st.chat_input("Ask something..."):
    mm_container = st.empty()
    user_msg = HumanMessage(content=prompt)
    def is_duplicate_user_message(user_msg, messages):
        return any(
            isinstance(msg, HumanMessage) and msg.content == user_msg.content
            for msg in messages
        )

    if not is_duplicate_user_message(user_msg, st.session_state.messages):
        mm_container.markdown(user_msg.content)
        st.session_state.messages.append(user_msg)

    input_state = {
        "messages": st.session_state.messages,
        "human_feedback": st.session_state.human_feedback
    }
    stream = app.stream(input_state, config=thread_config)
    print("The stream is running and the code is this\n", stream)
    with st.chat_message("assistant"):
        msg_container = st.empty()
        for chunk in stream:
            for node_id, value in chunk.items():
                if node_id == "__interrupt__":
                    print("[VALUE_0]",type(value[0].value))
                    print("[VALUE_0]",value[0].value)
                    # ai_msg = value[0].value
                    # print("value[0].value['messages'][-1]", ai_msg)
                    # msg_container.markdown(ai_msg)
                    msg_container.markdown(AIMessage(content=value[0].value))
                    st.session_state.messages.append(AIMessage(content = value[0].value))
                    st.session_state.phase = "waiting_feedback"
                    st.rerun()
                elif "messages" in value:
                    ai_msg = value["messages"][-1]
                    # Check if the message is an AIMessage
                    if isinstance(ai_msg, AIMessage):
                        msg_container.markdown(ai_msg.content)
                        st.session_state.messages.append(ai_msg)
                        st.rerun()


