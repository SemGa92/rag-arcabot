import streamlit as st



def get_sidebar(software: str):
    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This chatbot interfaces with a
            [LangChain](https://python.langchain.com/docs/get_started/introduction)
            agent designed to answer questions about Arca24's softwares.
            The agent uses retrieval-augment generation (RAG).
            """
        )

        with st.expander("Example Questions"):
            st.markdown(f"- What is {software}?")
            st.markdown( "- I lost my passowrd")
            st.markdown( "- I am a candidate. How can I apply for a job?")
            st.markdown(f"- Does {software} work on mobile phone?")
            st.markdown( "- How can I search for a candidate?")
            st.markdown( "- Can I customize the graphic?")
