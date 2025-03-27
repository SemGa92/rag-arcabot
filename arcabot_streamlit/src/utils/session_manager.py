import streamlit as st


def clear_msg_by_sw(software: str) -> None:
    if "software" in st.session_state:
        if st.session_state.software != software:
            st.session_state.software = software
            if "messages" in st.session_state:
                st.session_state.messages = []
    else:
        st.session_state.software = software

    if "messages" not in st.session_state:
        st.session_state.messages = []