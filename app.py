import streamlit as st
from components.login import tela_login
from components.lista import tela_lista
from components.cadastro import tela_cadastro
from session_state import init_session_state

# Inicializa o estado da sessão
init_session_state()

# Se estiver logado, mostra o menu lateral
if st.session_state.logado:
    st.sidebar.title("📋 Menu")
    pagina = st.sidebar.radio(
        "Navegação",
        ["Lista de Produtos", "Cadastrar Produto", "Sair"]
    )

    if pagina == "Lista de Produtos":
        tela_lista()
    elif pagina == "Cadastrar Produto":
        tela_cadastro()
    elif pagina == "Sair":
        st.session_state.logado = False
        st.session_state.token = None
        st.session_state.usuario = None
        st.session_state.loading_login = False
        st.rerun()
else:
    tela_login()
