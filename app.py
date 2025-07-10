import streamlit as st
from components.login import tela_login
from components.lista import tela_lista
from components.cadastro import tela_cadastro
from session_state import init_session_state

# Inicializa o estado da sessão
init_session_state()

# Função auxiliar para criar botões estilo link
def menu_link(texto, destino):
    estilo = """
        <style>
            .link-button {
                background-color: transparent;
                color: #3366cc;
                border: none;
                padding: 0.4rem 0;
                font-size: 1rem;
                text-align: left;
                cursor: pointer;
                width: 100%;
            }
            .link-button:hover {
                text-decoration: underline;
            }
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)
    return st.sidebar.button(texto, key=f"menu_{destino}", use_container_width=True)

# Verifica se o usuário está logado
if st.session_state.logado:
    # Garante que sempre comece na tela de lista
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "lista"

    nome_usuario = st.session_state.get("usuario", "Usuário")

    # Saudação com HTML no menu lateral
    st.sidebar.markdown(
        f"""
        <div style='margin-bottom: 2rem;'>
            <p style='font-weight: bold; font-size: 1.1rem;'>Olá, {nome_usuario}</p>
            <hr style='margin-top: 0.5rem;'>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Botões de navegação
    if menu_link("Lista de Produtos", "lista"):
        st.session_state.pagina_atual = "lista"
        st.rerun()
    if menu_link("Cadastrar Produto", "cadastro"):
        st.session_state.pagina_atual = "cadastro"
        st.rerun()

    # Espaço e botão de logout separado
    st.sidebar.markdown("<hr style='margin:1rem 0;'>", unsafe_allow_html=True)
    if menu_link("Sair", "sair"):
        st.session_state.logado = False
        st.session_state.token = None
        st.session_state.usuario = None
        st.session_state.loading_login = False
        st.session_state.pagina_atual = "login"
        st.rerun()

    # Renderiza a tela atual
    if st.session_state.pagina_atual == "lista":
        tela_lista()
    elif st.session_state.pagina_atual == "cadastro":
        tela_cadastro()

else:
    tela_login()
    if st.session_state.get("logado"):
        st.session_state.pagina_atual = "lista"
        st.rerun()
