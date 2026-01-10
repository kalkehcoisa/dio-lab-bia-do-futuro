#!/usr/bin/env bash

set -e

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements-dev.txt

if [ -z "$1" ]; then
    # Sem parâmetro: roda todos os testes
    pytest -v
else
    # Com parâmetro: roda teste específico
    pytest -v "$1"
fi