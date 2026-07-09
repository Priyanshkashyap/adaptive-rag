"""
Sidebar component.
"""
import streamlit as st

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
        st.code(st.session_state.session_id) # st.session_state is Streamlit's way of storing variables that persist across reruns.  st.code() displays text as a formatted code block(inside a box) in the Streamlit app.
        st.divider()

        if st.button("New Chat"):
            st.session_state.messages = []

        st.divider()
        uploaded_file = st.file_uploader("Upload Document",type=["pdf", "txt"],)
        description = st.text_input("Description")

        return uploaded_file, description