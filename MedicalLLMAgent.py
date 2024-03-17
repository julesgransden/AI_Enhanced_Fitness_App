from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_openai import ChatOpenAI
import streamlit as st
from streamlit_chat import message

def ChatBot():
    chat = ChatOpenAI(temperature=0,openai_api_key="OPEN_AI_KEY", )

    st.markdown("Chat with our personalized AI Medical chatbot **Toby** to get quick answers!! ")

    clear= st.button("Clear chat")
    if clear:
        st.session_state.messages = []

            
    if "messages" not in st.session_state:
        st.session_state.messages = [ 
                SystemMessage(content = "You are a helpful Medical assistant named Toby, to help me get quick treatment options for injuries I get while working out or doing sports")
            ]

    user_input = st.text_input("Explain what happened...", key="user_input")

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            st.session_state.text = ""
        
    messages = st.session_state.get('messages', [])
    for i,msg in enumerate(messages[1:]):
        if i %2 == 0:
            message(msg.content, is_user=True, key=str(i)+'_user')
        else:
            message(msg.content, is_user=False, key=str(i)+'_ai')
        