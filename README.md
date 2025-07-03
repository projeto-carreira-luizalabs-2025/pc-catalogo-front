# 📦 Frontend - Catálogo de Produtos (Streamlit)

Este é o frontend simples feito com **Streamlit** para interagir com a API do Catálogo de Produtos.

---

## 🖥️ Funcionalidades

- Visualizar a lista de produtos.
- Cadastrar e excluir produtos diretamente da interface.

---

## ⚙️ Pré-requisitos

Antes de iniciar, você precisará ter instalado:

- [Python 3.12](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [PIP](https://pip.pypa.io/)
- A API do Catálogo já rodando em `http://localhost:8000/api/docs`

---

## 🚀 Rodando o projeto

### 1. Clone o repositório

```bash
git clone https://https://github.com/projeto-carreira-luizalabs-2025/pc-catalogo.git
cd pc-catalogo-front
```

### 2. Execute a aplicação

Use o script já pronto para ativar o ambiente virtual e iniciar o Streamlit automaticamente:

```bash
python run_app.py
```

> 💡 Esse script também limpa os arquivos `__pycache__` antes de iniciar o frontend.

---

## 📁 Estrutura de Pastas

```
📦 PC-CATALOGO-FRONT
├── app.py              # Código principal da interface com Streamlit
├── run_app.py          # Script para rodar o app com setup completo
├── requirements.txt    # Dependências do projeto
├── utils.py            # Funções auxiliares para comunicação com a API
├── session_state.py    # Inicializador do estado da sessão do usuário
├── components/         # Telas da interface
│   ├── lista.py        # Tela de listagem de produtos
│   ├── cadastro.py     # Tela de cadastro de novo produto
│   └── login.py        # Tela de autenticação
└── README.md           # Instruções de uso
```

---

## ✅ Dicas

- Certifique-se de que a API esteja funcionando em `http://localhost:8000/api/docs`.