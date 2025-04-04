import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils.functions import file_request, get_pdf_preview



def select_software() -> None:
    software = st.selectbox(
        "Which software do you want to query?",
        ("Talentum", "Ngage", "JobArch", "JobCourier"),
    )
    st.session_state['software'] = software


def set_openai_token() -> None:
    with st.expander("OPENAI TOKEN", expanded=True, icon="🔑"):
        token = st.text_input(
            "Put your OpenAI token here",
            type='password'
        )
        if token:
            st.success(f'{token[:10]}..........{token[-10:]}')
            st.session_state['openai_token'] = token


def init_file_upload(
    key: str,
    label: str = 'Upload file',
    file_types: list = None
) -> UploadedFile:

    if key not in st.session_state:
        st.session_state[key] = {
            "file": None,
            "preview": None,
            "output": None,
            "error": None
        }

    uploaded_file = st.file_uploader(label, type=file_types, key=f"uploader_{key}")
    if uploaded_file is not None:
        if (st.session_state[key]["file"] is None or uploaded_file.name != st.session_state[key]["file"].name):
            st.session_state[key] = {
                "file": uploaded_file,
                "preview": None,
                "output": None,
                "error": None
            }

    return uploaded_file


def process_file_upload(key: str, uploaded_file: UploadedFile) -> None:
    with st.spinner("Processing..."):
        if st.session_state[key]["output"] is None:
            output, error = file_request(
                uploaded_file,
                st.session_state.get('software', ''),
                st.session_state.get('openai_token', '')
            )
            st.session_state[key]["output"] = output
            st.session_state[key]["error"] = error

        if st.session_state[key]["output"] and not st.session_state[key]["error"]:
            st.success(st.session_state[key]["output"]['message'])
            st.session_state['uid_chroma_collection'] = st.session_state[key]["output"]['uid']

            if st.session_state[key]["preview"] is None:
                file_bytes = uploaded_file.read()
                st.session_state[key]["preview"] = get_pdf_preview(file_bytes)

            st.image(st.session_state[key]["preview"], caption="PDF Preview", use_container_width=True)

        elif st.session_state[key]["error"]:
            st.error(st.session_state[key]["output"]['message'])
        else:
            st.error("Errore nell'elaborazione del file.")


def get_sidebar() -> str:
    """Configura la sidebar di Streamlit."""
    with st.sidebar:
        select_software()
        st.divider()

        set_openai_token()

        if 'openai_token' in st.session_state:
            f_key = 'db_update'
            st.divider()

            uploaded_file = init_file_upload(f_key, label='Update software DB', file_types=['pdf'])
            if uploaded_file:
                process_file_upload(f_key, uploaded_file)
