"""
Chat component.
"""
# displays the chat
import streamlit as st

def render_chat() -> None:
    """
    Render chat history.
    """
    st.title("Adaptive RAG Assistant")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])