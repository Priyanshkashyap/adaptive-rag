"""
Session utilities.
"""

import uuid

import streamlit as st
   # st.session_state is a Python dictionary maintained by Streamlit.It stores variables for the current user's Streamlit session.

def initialize_session() -> None:
    """
    Initialize Streamlit session state.
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "history_loaded" not in st.session_state:
        st.session_state.history_loaded = False


def start_new_chat() -> None:
    """
    Start a brand-new chat session.
    """
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.history_loaded = False


     