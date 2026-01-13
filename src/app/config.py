"""
Configurações do agente financeiro
"""
import os
from pathlib import Path
from typing import Set

# Caminhos
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
USUARIO_FILE = DATA_PATH / "usuario.json"
INTERACOES_PATH = DATA_PATH / "interacoes"

# Criar diretórios se não existirem
DATA_PATH.mkdir(exist_ok=True)
INTERACOES_PATH.mkdir(exist_ok=True)

# Campos permitidos para extração
CAMPOS_SUPORTADOS: Set[str] = {
    "renda_mensal",
    "perfil_investidor",
    "metas",
    "idade",
    "profissao",
    "patrimonio_total",
    "reserva_emergencia_atual"
}

# Perfis de investidor válidos
PERFIS_VALIDOS: Set[str] = {"conservador", "moderado", "arrojado"}

# Termos proibidos (aconselhamento financeiro)
TERMOS_PROIBIDOS = [
    "bitcoin",
    "invista",
    "investir",
    "recomendo",
    "compre",
    "venda",
    "aplique",
    "melhor investimento",
    "rentabilidade garantida",
    "vai subir",
    "vai cair",
    "lucro certo"
]

# Palavras de confirmação
PALAVRAS_CONFIRMACAO: Set[str] = {
    "sim",
    "confirmo",
    "ok",
    "pode salvar",
    "pode",
    "correto",
    "certo",
    "isso mesmo",
    "exato",
    "positivo"
}

# Palavras de negação
PALAVRAS_NEGACAO: Set[str] = {
    "não",
    "nao",
    "negativo",
    "cancel",
    "cancelar",
    "errado",
    "incorreto"
}

# LLM Configuration
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
GROQ_LLM_TIMEOUT = int(os.getenv("GROQ_LLM_TIMEOUT", LLM_TIMEOUT))

# Validação de valores
MIN_RENDA_MENSAL = 0.01
MAX_RENDA_MENSAL = 1_000_000.00
MIN_META_VALOR = 1.00
MAX_META_VALOR = 100_000_000.00
