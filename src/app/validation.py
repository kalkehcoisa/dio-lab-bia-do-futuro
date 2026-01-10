TERMOS_PROIBIDOS = [
    "invista",
    "investir em",
    "recomendo",
    "compre",
    "aplique em",
    "melhor investimento",
    "rentabilidade garantida"
]

CAMPOS_PERMITIDOS = {
    "renda_mensal",
    "perfil_investidor",
    "metas"
}


def extrair_fatos_permitidos(usuario: dict) -> set[str]:
    fatos = set()

    if not usuario:
        return fatos

    fatos.update([
        usuario.get("nome", ""),
        str(usuario.get("idade", "")),
        usuario.get("profissao", ""),
        str(usuario.get("renda_mensal", "")),
        str(usuario.get("patrimonio_total", "")),
        str(usuario.get("reserva_emergencia_atual", ""))
    ])

    perfil = usuario.get("perfil_investidor", {})
    if perfil.get("confirmado"):
        fatos.add(perfil.get("valor", ""))

    objetivo = usuario.get("objetivo_principal", {})
    if objetivo.get("confirmado"):
        fatos.add(objetivo.get("descricao", ""))

    for meta in usuario.get("metas", []):
        if meta.get("confirmado"):
            fatos.add(meta.get("meta", ""))
            fatos.add(str(meta.get("valor_necessario", "")))
            fatos.add(meta.get("prazo", ""))

    return {f for f in fatos if f}


def validar_resposta(novos_dados: dict, mensagem_original: str) -> tuple[bool, str | None]:
    texto = mensagem_original.lower()

    # 0. Bloqueio por linguagem proibida (aconselhamento financeiro)
    for termo in TERMOS_PROIBIDOS:
        if termo in texto:
            return (
                False,
                "Não posso fazer recomendações ou indicar investimentos específicos."
            )

    # 1. Campos inesperados
    for campo in novos_dados.keys():
        if campo not in CAMPOS_PERMITIDOS:
            return False, f"O campo '{campo}' não é permitido."

    # 2. Validação de renda
    if "renda_mensal" in novos_dados:
        renda = novos_dados["renda_mensal"]
        if not isinstance(renda, (int, float)) or renda <= 0:
            return False, "A renda mensal precisa ser um valor positivo."

    # 3. Perfil de investidor
    if "perfil_investidor" in novos_dados:
        if novos_dados["perfil_investidor"] not in {
            "conservador",
            "moderado",
            "arrojado"
        }:
            return False, "Perfil de investidor inválido."

    return True, None
