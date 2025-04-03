import streamlit as st
from utils.session_manager import clear_msg_by_sw
from utils.functions import chat_request



def get_chat():
    software = st.session_state['software']

    clear_msg_by_sw(software)

    for message in st.session_state.messages:
       with st.chat_message(message["role"]):
           if "output" in message.keys():
               st.markdown(message["output"])

    if prompt := st.chat_input("What do you want to know?"):
       st.chat_message("user").markdown(prompt)

       st.session_state.messages.append(
           {
               "role": "user",
               "output": prompt
            }
        )

       with st.spinner("Searching for an answer..."):
            data = {
                'text': prompt,
                'software': software,
                'openai_token': st.session_state['openai_token']
                }
            output_text, error = chat_request(data)

       if error:
          st.status("Error", state="error").error(output_text)
       else:
          st.chat_message("assistant").markdown(output_text)

       st.session_state.messages.append(
           {
               "role": "assistant",
               "output": output_text,
           }
       )
