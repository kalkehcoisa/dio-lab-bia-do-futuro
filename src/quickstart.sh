#!/usr/bin/env bash

set -e

echo "▶Iniciando ambiente do Agente Financeiro (DIO Lab)"

# --- Verificações básicas ---
command -v docker >/dev/null 2>&1 || {
  echo "❌ Docker não encontrado. Instale o Docker antes de continuar."
  exit 1
}

command -v docker-compose >/dev/null 2>&1 || {
  echo "❌ docker-compose não encontrado."
  exit 1
}

# --- Subindo os containers ---
echo "Subindo containers..."
docker-compose up -d

# --- Esperando Ollama ficar disponível ---
echo "Aguardando Ollama iniciar..."
until docker exec ollama ollama list >/dev/null 2>&1; do
  sleep 2
done

echo "Ollama pronto."

# --- Verificando modelo Phi-3 ---
MODEL_NAME="phi3"

if docker exec ollama ollama list | grep -q "$MODEL_NAME"; then
  echo "Modelo $MODEL_NAME já está disponível."
else
  echo "Baixando modelo $MODEL_NAME..."
  docker exec ollama ollama pull "$MODEL_NAME"
  echo "Modelo $MODEL_NAME baixado."
fi

# --- Finalização ---
echo ""
echo "Ambiente pronto!"
echo "Gradio: http://localhost:7860"
echo "Ollama API: http://localhost:11434"
echo ""
echo "Para parar tudo: docker-compose down"
