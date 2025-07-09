import os
import shutil
import subprocess
import platform
import sys

# -------------------------------------------------------------
# UTILITÁRIO PARA:
# 1) Limpar caches (__pycache__)
# 2) Criar venv (caso não exista)
# 3) Instalar dependências
# 4) Iniciar Streamlit (cross-platform)
# -------------------------------------------------------------

def apagar_pycaches(raiz="."):
    """
    Remove todas as pastas __pycache__ a partir do diretório raiz.
    """
    print("🔍 Limpando pastas __pycache__...")
    for root, dirs, _ in os.walk(raiz):
        for d in dirs:
            if d == "__pycache__":
                pasta = os.path.join(root, d)
                print(f"🗑️  Removendo: {pasta}")
                shutil.rmtree(pasta, ignore_errors=True)
    print("✅ Limpeza concluída.\n")


def criar_venv():
    """
    Cria um ambiente virtual em './venv' se ainda não existir.
    """
    if not os.path.isdir("venv"):
        print("🐍 Criando ambiente virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ Ambiente virtual criado.")
    else:
        print("✔️ Ambiente virtual já existe.")


def instalar_dependencias():
    """
    Instala dependências do requirements.txt usando o Python do venv.
    Funciona tanto no Windows quanto no Linux/macOS.
    """
    print("📦 Instalando dependências...")
    # Localiza o executável Python dentro do virtualenv
    if platform.system() == "Windows":
        py_exec = os.path.join("venv", "Scripts", "python.exe")
    else:
        py_exec = os.path.join("venv", "bin", "python")
    subprocess.check_call([py_exec, "-m", "pip", "install", "-r", "requirements.txt"] )
    print("✅ Dependências instaladas.")


def iniciar_streamlit():
    """
    Executa Streamlit via Python do venv, sem precisar ativar o shell.
    Compatível com Windows, Linux e macOS.
    """
    print("🚀 Iniciando Streamlit...")
    if platform.system() == "Windows":
        py_exec = os.path.join("venv", "Scripts", "python.exe")
    else:
        py_exec = os.path.join("venv", "bin", "python")

    # Chama streamlit como módulo
    subprocess.run([py_exec, "-m", "streamlit", "run", "app.py"] )


if __name__ == "__main__":
    apagar_pycaches()
    criar_venv()
    instalar_dependencias()
    iniciar_streamlit()
