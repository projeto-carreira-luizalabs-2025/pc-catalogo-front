import requests
import streamlit as st

API_URL = "http://localhost:8000/seller/v2/catalogo"

import streamlit as st

def get_headers():
    token = st.session_state.get("token", "")
    seller_id = "magalu"
    headers = {
        "x-seller-id": seller_id,
        "Authorization": f"Bearer {token}"
    }
    return headers

def get_produtos(name_like=None, limit=50, offset=0, sort=None):
    try:
        params = {
            "_limit": limit,
            "_offset": offset
        }
        if name_like:
            params["name_like"] = name_like
        if sort:
            params["_sort"] = sort

        resp = requests.get(API_URL, headers=get_headers(), params=params)
        if resp.status_code == 200:
            return resp.json().get("results", [])
        return []
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

def get_produto_por_sku(sku):
    try:
        resp = requests.get(f"{API_URL}/{sku}", headers=get_headers())
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        print(f"Erro ao buscar produto {sku}: {e}")
        return None

def cadastrar_produto(sku, nome):
    try:
        payload = {"sku": sku, "name": nome}
        resp = requests.post(API_URL, headers=get_headers(), json=payload)

        if resp.status_code == 201:
            return True, None
        else:
            try:
                data = resp.json()
                detalhes = data.get("details", [])
                if detalhes and isinstance(detalhes, list):
                    mensagem_erro = detalhes[0].get("message", "Erro desconhecido")
                else:
                    mensagem_erro = data.get("message", "Erro desconhecido")
            except Exception:
                mensagem_erro = "Erro desconhecido ao processar a resposta da API"

            return False, mensagem_erro

    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        return False, str(e)

def atualizar_produto(sku, nome=None, description=None):
    try:
        payload = {}
        if nome is not None:
            payload["name"] = nome
        if description is not None:
            payload["description"] = description
        if not payload:
            return False, "Nenhuma alteração fornecida."

        resp = requests.patch(f"{API_URL}/{sku}", headers=get_headers(), json=payload)

        if resp.status_code == 202:
            return True, None
        else:
            try:
                data = resp.json()
                detalhes = data.get("details", [])
                if detalhes and isinstance(detalhes, list):
                    mensagem_erro = detalhes[0].get("message", "Erro desconhecido")
                else:
                    mensagem_erro = data.get("message", "Erro desconhecido")
            except Exception:
                mensagem_erro = "Erro desconhecido ao processar a resposta da API"
            return False, mensagem_erro

    except Exception as e:
        print(f"Erro ao atualizar produto {sku}: {e}")
        return False, str(e)

def excluir_produto(sku):
    try:
        resp = requests.delete(f"{API_URL}/{sku}", headers=get_headers())
        return resp.status_code == 204
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")
        return False
