import streamlit as st

from components.sidebar import get_sidebar
from components.intro import get_intro
from components.chat import get_chat


st.set_page_config(
    page_title="ARCA-BOT",
    page_icon="🤖"
    )


get_sidebar()
get_intro()

if 'uid' in st.session_state:
    st.write(st.session_state['uid'])

if 'openai_token' in st.session_state:
    get_chat()
