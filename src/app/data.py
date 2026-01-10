import json
import os
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
USUARIO_FILE = os.path.join(BASE_PATH, "data", "usuario.json")


def aplicar_atualizacoes(usuario: dict, updates: dict) -> dict:
    for chave, valor in updates.items():
        if chave == "perfil_investidor":
            usuario["perfil_investidor"] = valor
        elif chave == "renda_mensal":
            usuario["renda_mensal"] = valor
        elif chave == "metas":
            usuario["metas"].extend(valor)

    return usuario


def carregar_usuario() -> dict:
    if not os.path.exists(USUARIO_FILE):
        usuario = usuario_padrao()
        salvar_usuario(usuario)
        return usuario

    with open(USUARIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def resumo_usuario(usuario):
    if not usuario:
        return "📋 Perfil ainda vazio."

    linhas = ["📋 **Resumo do seu perfil:**"]
    for k, v in usuario.items():
        linhas.append(f"- **{k}**: {v}")
    return "\n".join(linhas)


def salvar_usuario(usuario: dict):
    usuario["ultima_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(USUARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(usuario, f, ensure_ascii=False, indent=2)


def usuario_padrao() -> dict:
    return {
        "perfil_investidor": None,
        "renda_mensal": None,
        "metas": [],
        "ultima_atualizacao": None
    }
