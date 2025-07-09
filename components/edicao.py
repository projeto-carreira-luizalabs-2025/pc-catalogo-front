import streamlit as st
from utils import atualizar_produto

def tela_edicao():
    produto = st.session_state.get('produto_editar')

    if not produto:
        st.warning("Nenhum produto selecionado para edição.")
        return

    st.title("✏️ Editar Produto")
    st.markdown(f"**SKU:** `{produto['sku']}`")

    nome = st.text_input("Nome", value=produto['name'])
    descricao = st.text_area("Descrição", value=produto.get('description', ''))

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Salvar alterações"):
            if atualizar_produto(produto['sku'], nome=nome, description=descricao):
                st.success("Produto atualizado com sucesso!")
                st.session_state['modo_edicao'] = False
                st.session_state['produto_editar'] = None
                st.rerun()
            else:
                st.error("Erro ao atualizar produto.")

    with col2:
        if st.button("❌ Cancelar"):
            st.session_state['modo_edicao'] = False
            st.session_state['produto_editar'] = None
            st.rerun()
