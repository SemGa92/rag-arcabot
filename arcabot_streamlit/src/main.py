import os
import streamlit as st

from utils.functions import get_sw_dir



st.set_page_config(
    page_title="ARCA-BOT",
    page_icon="🤖"
    )


jb_page = st.Page(get_sw_dir("jobarch.py"), title="JOBARCH", icon=":material/star:")
ng_page = st.Page(get_sw_dir("ngage.py"), title="NGAGE",icon=":material/star:")
tl_page = st.Page(get_sw_dir("talentum.py"), title="TALENTUM", icon=":material/star:")
jc_page = st.Page(get_sw_dir("jobcourier.py"), title="JOBCOURIER", icon=":material/star:")
logout_page = st.Page("components/logout.py", title="Log out", icon=":material/logout:")

pg = st.navigation(
   {
       "Software": [jb_page, ng_page, tl_page, jc_page],
       "Account": [logout_page],
   }
)
pg.run()
