import streamlit as st
from utils import get_produtos, excluir_produto
from components.edicao import tela_edicao

def tela_lista():
    if st.session_state.get("modo_edicao") and st.session_state.get("produto_editar"):
        tela_edicao()
        return

    st.title("📦 Lista de Produtos")
    
    produtos = get_produtos()
    if not produtos:
        st.info("Nenhum produto cadastrado.")
    else:
        for p in produtos:
            with st.expander(f"📦 {p['name']}"):
                st.markdown(f"**SKU:** `{p['sku']}`")
                st.markdown(f"**Descrição:** {p.get('description', '—')}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Editar", key=f"editar-{p['sku']}"):
                        st.session_state["modo_edicao"] = True
                        st.session_state["produto_editar"] = p
                        st.rerun()

                with col2:
                    if st.button("🗑️ Excluir", key=f"excluir-{p['sku']}"):
                        if excluir_produto(p['sku']):
                            st.success("Produto excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir produto.")

                st.markdown("---")
