import streamlit as st


def get_intro():
    software = st.session_state['software']

    st.title(f"{software}-bot".upper())
    st.info(
       f"Ask me questions about {software} software provided by Arca24. "
       "I can give you assistance on basic doubts or operations!"
    )

    st.session_state['custom_prompt'] = st.text_area(
        "Custom Prompt",
        f"""You are a Customer Service Assistant knowledgeable {software}, an HR software developed by Arca24. """
        f"""You can help users answering questions only about {software} features and functionalities. """
        f"""Use the following context to answer questions. Be as detailed as possible, but don't make up any information that's not from the context. """
        f"""If you don't know an answer, say you don't know. You must not answer questions not related to {software}.""",
        height=150
    )
