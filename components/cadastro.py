import streamlit as st
from utils import cadastrar_produto

def tela_cadastro():
    st.title("📦 Cadastrar Produto")

    sku = st.text_input("SKU do Produto")
    nome = st.text_input("Nome do Produto")

    if st.button("Cadastrar"):
        if not sku or not nome:
            st.warning("Preencha todos os campos.")
        else:
            with st.spinner("Cadastrando produto..."):
                sucesso = cadastrar_produto(sku, nome)

            if sucesso:
                st.success("Produto cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar produto.")
