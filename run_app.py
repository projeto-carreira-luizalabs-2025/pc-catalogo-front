import os
import shutil
import subprocess
import platform
import sys

def apagar_pycaches(raiz="."):
    print("🔍 Limpando pastas __pycache__...")
    for root, dirs, _ in os.walk(raiz):
        for d in dirs:
            if d == "__pycache__":
                pasta = os.path.join(root, d)
                print(f"🗑️  Removendo: {pasta}")
                shutil.rmtree(pasta, ignore_errors=True)
    print("✅ Limpeza concluída.\n")

def criar_venv():
    if not os.path.isdir("venv"):
        print("🐍 Criando ambiente virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ Ambiente virtual criado.")
    else:
        print("✔️ Ambiente virtual já existe.")

def instalar_dependencias():
    print("📦 Instalando dependências...")
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("✅ Dependências instaladas.")

def iniciar_streamlit():
    print("🚀 Iniciando Streamlit com ambiente virtual...")
    sistema = platform.system()
    if sistema == "Windows":
        comando = (
            'cmd.exe /k "venv\\Scripts\\activate && streamlit run app.py"'
        )
        subprocess.run(comando, shell=True)
    else:
        comando = 'source venv/bin/activate && streamlit run app.py'
        subprocess.run(comando, shell=True, executable='/bin/bash')

if __name__ == "__main__":
    apagar_pycaches()
    criar_venv()
    instalar_dependencias()
    iniciar_streamlit()
