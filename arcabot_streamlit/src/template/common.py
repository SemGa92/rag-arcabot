from components.sidebar import get_sidebar
from components.intro import get_intro
from components.chat import get_chat



def common_template(software: str) -> None:
    get_sidebar(software)
    get_intro(software)
    get_chat(software)
