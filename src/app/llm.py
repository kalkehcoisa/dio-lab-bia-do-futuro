import subprocess
from typing import Set


def gerar_resposta(mensagem_usuario: str, fatos_permitidos: Set[str]) -> str:
    contexto = "\n".join(f"- {f}" for f in fatos_permitidos)

    prompt = f"""
Você é um assistente financeiro educacional.
Você NÃO pode fazer recomendações de investimento.
Você SÓ pode usar os fatos abaixo.

FATOS PERMITIDOS:
{contexto}

Pergunta do usuário:
{mensagem_usuario}

Se a resposta não puder ser baseada apenas nos fatos permitidos,
diga claramente que não tem informação suficiente.
"""

    result = subprocess.run(
        ["ollama", "run", "phi3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()
