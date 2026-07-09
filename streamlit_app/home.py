"""
Adaptive RAG UI.
"""

import streamlit as st
from components.sidebar import render_sidebar
from components.chat import render_chat
from utils.api_client import (ask_question,upload_document,)
from utils.session import (initialize_session,)

st.set_page_config(page_title="Adaptive RAG",page_icon="🤖",layout="wide",)
initialize_session()
uploaded_file, description = render_sidebar()
render_chat()

if uploaded_file:

    if st.button("Upload"):

        with st.spinner(
            "Uploading..."
        ):

            try:

                result = upload_document(
                    uploaded_file,
                    description,
                )

                st.success(
                    f"{result['filename']} uploaded successfully."
                )

            except Exception as error:

                st.error(str(error))


prompt = st.chat_input(
    "Ask something..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.spinner(
        "Thinking..."
    ):

        try:

            response = ask_question(
                prompt,
                st.session_state.session_id,
            )

            answer = response["answer"]

        except Exception as error:

            answer = str(error)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.rerun()