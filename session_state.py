import streamlit as st

def init_session_state():
    if "logado" not in st.session_state:
        st.session_state.logado = False
    if "usuario" not in st.session_state:
        st.session_state.usuario = ""
    if "token" not in st.session_state:
        st.session_state.token = ""
    if "sellerid" not in st.session_state:
        st.session_state.sellerid = ""
