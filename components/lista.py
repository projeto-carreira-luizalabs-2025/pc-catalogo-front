import streamlit as st
from utils import get_produtos, excluir_produto

def tela_lista():
    st.title("📦 Lista de Produtos")

    produtos = get_produtos()
    if not produtos:
        st.info("Nenhum produto cadastrado.")
    else:
        for p in produtos:
            with st.container():
                col1, col2, col3 = st.columns([3, 4, 1])
                
                with col1:
                    st.markdown("**SKU:**")
                    st.code(p['sku'], language="text")
                
                with col2:
                    st.markdown("**Nome:**")
                    st.write(p['name'])

                with col3:
                    st.markdown("### ")
                    if st.button("🗑️ Excluir", key=p['sku']):
                        if excluir_produto(p['sku']):
                            st.success("Produto excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir produto.")

                st.markdown("---")
