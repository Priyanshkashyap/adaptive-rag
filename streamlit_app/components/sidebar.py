"""
Sidebar component.
"""
import streamlit as st
from utils.session import start_new_chat

def render_sidebar():
    """
    Render sidebar.

    Returns:
        Uploaded file and description.
    """
    with st.sidebar:
        st.title("Adaptive RAG")

        st.divider()

        st.subheader("Current Session")
        st.code(st.session_state.session_id)

        st.divider()

        if st.button("New Chat"):
            start_new_chat()
            st.rerun()

        st.divider()

        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "txt"],
            key=f"uploader_{st.session_state.session_id}",
        )

        description = st.text_input(
            "Description",
            key=f"description_{st.session_state.session_id}",
        )

        return uploaded_file, description