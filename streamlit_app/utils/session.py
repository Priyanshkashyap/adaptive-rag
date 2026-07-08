"""
Session utilities.
"""
import uuid
import streamlit as st

def initialize_session() -> None:
    """
    Initialize Streamlit session state.
    """

    if "session_id" not in st.session_state: # st.session_state is a Python dictionary maintained by Streamlit.It stores variables for the current user's Streamlit session.
        st.session_state.session_id = str( # if session not there then generate
            uuid.uuid4()
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []