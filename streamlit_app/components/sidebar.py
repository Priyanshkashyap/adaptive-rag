"""
Sidebar component.
"""
import streamlit as st

def render_sidebar() -> None:
    """
    Render application sidebar.
    """
    with st.sidebar: # in the sidebar section there is headings title subheader etc.

        st.title("Adaptive RAG")
        st.divider()
        st.subheader("Current Session")
        st.code(st.session_state.session_id)
        st.divider()
        if st.button("New Chat"): # if this button is clicked
            st.session_state.messages = []
        st.divider()
        st.file_uploader("Upload Document",type=["pdf", "txt"],disabled=True,)