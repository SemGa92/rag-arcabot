import streamlit as st


def get_intro():
    software = st.session_state['software']

    st.title(f"{software}-bot".upper())
    st.info(
       f"Ask me questions about {software} software provided by Arca24. "
       "I can give you assistance on basic doubts or operations!"
    )