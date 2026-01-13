#!/usr/bin/env bash

set -e


echo "▶ Iniciando ambiente do Agente Financeiro (DIO Lab)"

# --- Verificações básicas ---
command -v python3.11 >/dev/null 2>&1 || {
  echo "❌ Python3.11 não encontrado. Instale antes de continuar."
  exit 1
}

# --- Criando venv se não existir ---
if [ ! -d "src/app/.venv" ]; then
  echo "Criando virtualenv..."
  python3.11 -m venv src/app/.venv
fi

# --- Ativando venv ---
echo "Ativando virtualenv..."
source src/app/.venv/bin/activate

# --- Atualizando pip ---
pip install --upgrade pip >/dev/null

# --- Instalando dependências ---
if [ -f "src/app/requirements.txt" ]; then
  echo "Instalando dependências..."
  pip install -r src/app/requirements.txt
else
  echo "❌ requirements.txt não encontrado."
  exit 1
fi

if [ -z "src/app/.env" ]; then
  echo "❌ arquivo .env não encontrado."
  echo "Necessário para carregar as variáveis de ambiente."
  exit 1
fi

# --- Subindo aplicação ---
echo ""
echo "Iniciando aplicação Gradio..."
echo "URL: http://localhost:7860"
echo ""

python src/app/main.py