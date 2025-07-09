import streamlit as st
from utils import get_produtos, excluir_produto
from components.edicao import tela_edicao

def tela_lista():
    if st.session_state.get("modo_edicao") and st.session_state.get("produto_editar"):
        tela_edicao()
        return

    st.title("📦 Lista de Produtos")

    # Inicialização de estado
    if "pagina" not in st.session_state:
        st.session_state.pagina = 0
    if "filtro_anterior" not in st.session_state:
        st.session_state.filtro_anterior = ""
    if "sort_anterior" not in st.session_state:
        st.session_state.sort_anterior = "name:asc"
    if "itens_por_pagina_anterior" not in st.session_state:
        st.session_state.itens_por_pagina_anterior = 10

    # Filtro e ordenação
    sort_opcoes = ["name:asc", "name:desc", "sku:asc", "sku:desc"]
    sort_labels = {
        "name:asc": "Nome (A-Z)",
        "name:desc": "Nome (Z-A)",
        "sku:asc": "SKU (Crescente)",
        "sku:desc": "SKU (Decrescente)"
    }

    col_filtro, col_sort = st.columns([3, 1])
    with col_filtro:
        nome_filtro = st.text_input("🔍 Buscar por nome:", value=st.session_state.filtro_anterior)

    with col_sort:
        sort_opcao = st.selectbox(
            "Ordenar por:",
            options=sort_opcoes,
            index=0,
            format_func=lambda x: sort_labels.get(x, x)
        )

    # Itens por página
    itens_por_pagina_opcoes = [5, 10, 20, 50]
    itens_atual = st.session_state.get("itens_por_pagina_anterior", 10)
    if itens_atual not in itens_por_pagina_opcoes:
        itens_atual = 10

    itens_por_pagina = st.selectbox(
        "Itens por página:",
        itens_por_pagina_opcoes,
        index=itens_por_pagina_opcoes.index(itens_atual),
        key="itens_por_pagina"
    )

    # Detecta mudanças e reseta a página
    if (
        nome_filtro != st.session_state.filtro_anterior or
        sort_opcao != st.session_state.get("sort_anterior", "") or
        itens_por_pagina != st.session_state.itens_por_pagina_anterior
    ):
        st.session_state.pagina = 0
        st.session_state.filtro_anterior = nome_filtro
        st.session_state.sort_anterior = sort_opcao  # Atualiza aqui corretamente
        st.session_state.itens_por_pagina_anterior = itens_por_pagina
        st.rerun()

    # Calcular offset
    offset = st.session_state.pagina * itens_por_pagina

    # Buscar produtos
    produtos = get_produtos(
        name_like=nome_filtro,
        limit=itens_por_pagina,
        offset=offset,
        sort=sort_opcao
    )

    # Exibição
    if not produtos:
        st.info("Nenhum produto encontrado.")
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

        st.divider()

        # Paginação
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Anterior", disabled=st.session_state.pagina == 0):
                st.session_state.pagina -= 1
                st.rerun()

        with col2:
            st.markdown(
                f"<p style='text-align:center;'>Página <b>{st.session_state.pagina + 1}</b></p>",
                unsafe_allow_html=True
            )

        with col3:
            if st.button("➡️ Próxima", disabled=len(produtos) < itens_por_pagina):
                st.session_state.pagina += 1
                st.rerun()
