import re
from typing import Dict, Any

CAMPOS_SUPORTADOS = {
    "renda_mensal",
    "perfil_investidor",
    "metas"
}

PERFIS_VALIDOS = {"conservador", "moderado", "arrojado"}


def extrair_renda_mensal(texto):
    # Padrão amplo para valores BR: R$, reais, números com . ou , decimais
    padrao_valor = r'(?:[Rr]\$?|reais?|R\$)?\s*([\d.]+(?:,\d{2})?)|(\d+(?:[.,]\d{2})?)\s*(?:reais?|R\$|[Rr]\$?)'
    
    matches = re.findall(padrao_valor, texto, re.IGNORECASE)
    
    candidatos = []
    for match in matches:
        for grupo in match:
            if grupo and re.match(r'\d', grupo):  # Garante numérico
                valor_str = re.sub(r'\.', '', grupo)  # Remove . milhares
                valor_str = valor_str.replace(',', '.')  # , para .
                try:
                    valor = float(valor_str)
                    if 100 < valor < 100000:  # Plausível para renda mensal
                        candidatos.append(valor)
                except ValueError:
                    pass
    
    # Prioriza valores próximos a palavras-chave de renda
    palavras_chave = ['renda', 'salário', 'ganho', 'recebo', 'lucro']
    if any(palavra in texto.lower() for palavra in palavras_chave):
        return max(candidatos) if candidatos else None
    return max(candidatos) if candidatos else None


def detectar_novos_dados(texto: str) -> Dict[str, Any]:
    texto = texto.lower()
    dados: Dict[str, Any] = {}

    # Renda mensal
    match = extrair_renda_mensal(texto)
    if match:
        dados["renda_mensal"] = float(match.group().replace(",", "."))

    # Perfil de investidor
    for perfil in PERFIS_VALIDOS:
        if f"perfil {perfil}" in texto or f"sou {perfil}" in texto:
            dados["perfil_investidor"] = perfil
            break

    # patrimônio explícito
    patrimonio = re.search(r"patrim[oô]nio.*?(\d+[.,]?\d*)", texto, re.IGNORECASE)
    if patrimonio:
        dados["patrimonio_total"] = float(patrimonio.group(1).replace(",", "."))

    # Metas financeiras
    # Exemplo explícito: "meta de juntar 20000 até 2026"
    meta_match = re.search(
        r"meta.*?(\d{1,3}(\.\d{3})*|\d+).*(\d{4})",
        texto
    )
    if meta_match:
        valor = meta_match.group(1).replace(".", "")
        prazo = meta_match.group(3)

        dados["metas"] = [{
            "meta": "Meta informada pelo usuário",
            "valor_necessario": float(valor),
            "prazo": prazo
        }]

    # reserva de emergência explícita
    reserva = re.search(r"reserva.*?(\d+[.,]?\d*)", texto, re.IGNORECASE)
    if reserva:
        dados["reserva_emergencia_atual"] = float(reserva.group(1).replace(",", "."))

    return dados


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
