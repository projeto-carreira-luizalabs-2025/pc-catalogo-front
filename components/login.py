import streamlit as st
import requests

from utils import get_attributes

KEYCLOAK_URL = "http://localhost:8080/realms/marketplace/protocol/openid-connect/token"
CLIENT_ID = "varejo"

def tela_login():
    if st.session_state.get("loading_login"):
        with st.spinner("Autenticando..."):
            username = st.session_state.get("username_input", "")
            password = st.session_state.get("password_input", "")

            payload = {
                "client_id": CLIENT_ID,
                "username": username,
                "password": password,
                "grant_type": "password",
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            try:
                response = requests.post(KEYCLOAK_URL, data=payload, headers=headers)
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    st.session_state.logado = True
                    st.session_state.usuario = username
                    st.session_state.loading_login = False
                    st.session_state.sellerid= get_attributes().get("sellers")
                    print(st.session_state.sellerid)
                    st.rerun()
                else:
                    st.session_state.loading_login = False
                    st.error("Usuário ou senha inválidos.")
                    print(response.text)
            except Exception as e:
                st.session_state.loading_login = False
                st.error(f"Erro ao autenticar: {e}")
        return

    st.markdown("<h1 style='text-align: center;'>Login no Catálogo</h1>", unsafe_allow_html=True)
    st.write("Faça login com seu usuário e senha")

    username = st.text_input("Usuário", key="username_input")
    password = st.text_input("Senha", type="password", key="password_input")

    if st.button("Entrar"):
        if not username or not password:
            st.warning("Preencha todos os campos.")
        else:
            st.session_state.loading_login = True
            st.rerun()
