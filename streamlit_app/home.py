"""
Adaptive RAG UI.
"""
import streamlit as st
from streamlit_app.components.chat import (render_chat,)
from streamlit_app.components.sidebar import (render_sidebar,)
from streamlit_app.utils.session import (initialize_session,)

st.set_page_config(page_title="Adaptive RAG",page_icon="🤖",layout="wide",)

initialize_session()
render_sidebar()
render_chat()

prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "Backend integration "
                "will be added on Day 15."
            ),
        }
    )

    st.rerun()