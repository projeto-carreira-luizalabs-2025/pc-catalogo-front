import streamlit as st
from utils import cadastrar_produto

def tela_cadastro():
    st.markdown("<h2 style='text-align: center;'>Cadastrar Produto</h2>", unsafe_allow_html=True)

    sku = st.text_input("SKU do Produto")
    nome = st.text_input("Nome do Produto")

    if st.button("Cadastrar"):
        if not sku or not nome:
            st.warning("Preencha todos os campos.")
        else:
            if cadastrar_produto(sku, nome):
                st.success("Produto cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar produto.")
