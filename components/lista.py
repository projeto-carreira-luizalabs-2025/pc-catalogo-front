import streamlit as st
from utils import get_produtos, get_produto_por_sku, excluir_produto
from components.edicao import tela_edicao

def tela_lista():
    if st.session_state.get("modo_edicao") and st.session_state.get("produto_editar"):
        tela_edicao()
        return

    st.title("📦 Lista de Produtos")

    # Inicialização de estados da sessão
    st.session_state.setdefault("pagina", 0)
    st.session_state.setdefault("filtro_nome_anterior", "")
    st.session_state.setdefault("filtro_sku_anterior", "")
    st.session_state.setdefault("sort_anterior", "name:asc")
    st.session_state.setdefault("itens_por_pagina_anterior", 10)

    sort_opcoes = ["name:asc", "name:desc", "sku:asc", "sku:desc"]
    sort_labels = {
        "name:asc": "Nome (A-Z)",
        "name:desc": "Nome (Z-A)",
        "sku:asc": "SKU (Crescente)",
        "sku:desc": "SKU (Decrescente)"
    }

    # Linha de filtros (nome e SKU)
    col1, col_meio, col2 = st.columns([3, 0.5, 3])
    with col1:
        nome_filtro = st.text_input("🔍 Nome:", value=st.session_state.filtro_nome_anterior)
    with col_meio:
        st.markdown(
            "<div style='text-align:center; padding-top:2.3rem; font-weight:bold; color:gray;'>ou</div>",
            unsafe_allow_html=True
        )
    with col2:
        sku_filtro = st.text_input("🔍 SKU:", value=st.session_state.filtro_sku_anterior)

    # Linha com selects (ordenar e quantidade), alinhados à direita
    _, col_sort, col_qtd = st.columns([3.5, 1.5, 1.5])

    with col_sort:
        sort_opcao = st.selectbox(
            "Ordenar:",
            options=sort_opcoes,
            index=sort_opcoes.index(st.session_state.sort_anterior),
            format_func=lambda x: sort_labels.get(x, x),
            key="sort"
        )

    with col_qtd:
        nova_qtd = st.selectbox(
            "Qtd/página:",
            [5, 10, 20, 50],
            index=[5, 10, 20, 50].index(st.session_state.itens_por_pagina_anterior),
            key="itens_por_pagina"
        )

    # Detectar mudanças de filtro
    if (
        nome_filtro != st.session_state.filtro_nome_anterior or
        sku_filtro != st.session_state.filtro_sku_anterior or
        sort_opcao != st.session_state.sort_anterior or
        nova_qtd != st.session_state.itens_por_pagina_anterior
    ):
        st.session_state.pagina = 0
        st.session_state.filtro_nome_anterior = nome_filtro
        st.session_state.filtro_sku_anterior = sku_filtro
        st.session_state.sort_anterior = sort_opcao
        st.session_state.itens_por_pagina_anterior = nova_qtd
        st.rerun()

    # Buscar produtos
    produtos = []
    if sku_filtro:
        produto = get_produto_por_sku(sku_filtro.strip())
        if produto:
            produtos = [produto]
        else:
            st.warning("Produto com esse SKU não encontrado.")
    else:
        offset = st.session_state.pagina * st.session_state.itens_por_pagina_anterior
        produtos = get_produtos(
            name_like=nome_filtro,
            limit=st.session_state.itens_por_pagina_anterior,
            offset=offset,
            sort=sort_opcao
        )

    # Exibição dos produtos
    if not produtos:
        st.info("Nenhum produto encontrado.")
    else:
        for i, p in enumerate(produtos):
            with st.expander(f"📦 {p['name']}"):
                st.markdown(f"**SKU:** `{p['sku']}`")
                st.markdown(f"**Descrição:** {p.get('description', '—')}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Editar", key=f"editar-{p['sku']}-{i}"):
                        st.session_state["modo_edicao"] = True
                        st.session_state["produto_editar"] = p
                        st.rerun()
                with col2:
                    if st.button("🗑️ Excluir", key=f"excluir-{p['sku']}-{i}"):
                        if excluir_produto(p['sku']):
                            st.success("Produto excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir produto.")

    # Paginação (somente quando NÃO busca por SKU)
    if not sku_filtro:
        st.divider()
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            st.button(
                "⬅️ Anterior",
                disabled=st.session_state.pagina == 0,
                on_click=lambda: st.session_state.update(pagina=st.session_state.pagina - 1),
                key="botao_anterior"
            )

        with col2:
            st.markdown(
                f"<p style='text-align:center; font-weight:bold;'>Página <b>{st.session_state.pagina + 1}</b></p>",
                unsafe_allow_html=True
            )

        with col3:
            subcol1, subcol2 = st.columns([1, 1])
            with subcol2:
                st.button(
                    "Próxima ➡️",
                    disabled=len(produtos) < st.session_state.itens_por_pagina_anterior,
                    on_click=lambda: st.session_state.update(pagina=st.session_state.pagina + 1),
                    key="botao_proxima"
                )
