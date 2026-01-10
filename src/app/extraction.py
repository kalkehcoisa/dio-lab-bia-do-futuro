"""
Extração de dados estruturados de texto natural
"""
import re
from typing import Dict, Any, Set, Optional, List

from .config import CAMPOS_SUPORTADOS, PERFIS_VALIDOS
from .exceptions import ExtractionError


class DataExtractor:
    """Extrator de dados estruturados de mensagens do usuário"""

    def __init__(self):
        self.campos_suportados = CAMPOS_SUPORTADOS
        self.perfis_validos = PERFIS_VALIDOS

    def detectar_novos_dados(self, texto: str) -> Dict[str, Any]:
        """
        Detecta e extrai novos dados da mensagem do usuário.

        Args:
            texto: Mensagem do usuário

        Returns:
            Dicionário com dados extraídos

        Raises:
            ExtractionError: Se houver erro na extração
        """
        if not texto or not isinstance(texto, str):
            return {}

        try:
            texto_lower = texto.lower()
            dados: Dict[str, Any] = {}

            # Extrai renda mensal
            renda = self._extrair_renda(texto_lower)
            if renda is not None:
                dados["renda_mensal"] = renda

            # Extrai perfil de investidor
            perfil = self._extrair_perfil(texto_lower)
            if perfil:
                dados["perfil_investidor"] = perfil

            # Extrai metas
            metas = self._extrair_metas(texto_lower, texto)
            if metas:
                dados["metas"] = metas

            # Extrai idade
            idade = self._extrair_idade(texto_lower)
            if idade is not None:
                dados["idade"] = idade

            # Extrai profissão
            profissao = self._extrair_profissao(texto)
            if profissao:
                dados["profissao"] = profissao

            # Extrai patrimônio
            patrimonio = self._extrair_patrimonio(texto_lower)
            if patrimonio is not None:
                dados["patrimonio_total"] = patrimonio

            # Extrai reserva de emergência
            reserva = self._extrair_reserva_emergencia(texto_lower)
            if reserva is not None:
                dados["reserva_emergencia_atual"] = reserva

            return dados

        except Exception as e:
            raise ExtractionError(f"Erro ao extrair dados: {e}")

    def _extrair_renda(self, texto: str) -> Optional[float]:
        """Extrai valor de renda mensal"""
        patterns = [
            r"(?:renda|sal[aá]rio|ganho).*?(?:de|é|:)?\s*r?\$?\s*(-?\d+(?:\.\d{3})*(?:,\d{2})?)",
            r"(?:renda|sal[aá]rio|ganho).*?(-?\d+(?:\.\d{3})*(?:,\d{2})?)\s*(?:reais|por\s+m[eê]s)",
        ]

        for pattern in patterns:
            match = re.search(pattern, texto.lower())
            if match:
                valor_str = match.group(1).replace(".", "").replace(",", ".")
                return float(valor_str)

        return None

    def _extrair_perfil(self, texto: str) -> Optional[str]:
        """Extrai perfil de investidor"""
        for perfil in self.perfis_validos:
            patterns = [
                rf"perfil\s+{perfil}",
                rf"perfil\s+é\s+{perfil}",
                rf"sou\s+{perfil}",
                rf"{perfil}\s+investidor",
                rf"investidor\s+{perfil}",
                rf"me\s+considero.*?{perfil}",
            ]
            for pattern in patterns:
                if re.search(pattern, texto):
                    return perfil

        return None

    def _extrair_metas(self, texto_lower: str, texto_original: str) -> Optional[List]:
        """Extrai metas financeiras"""
        metas = []

        # Padrão: "meta de juntar 20000 até 2026"
        pattern1 = (
            r"(?:meta|juntar|economizar|guardar).*?"
            r"r?\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?).*?"
            r"(?:at[eé]|para)?\s*(\d{4})"
        )
        matches = re.finditer(pattern1, texto_lower)

        for match in matches:
            valor_str = match.group(1).replace(".", "")
            prazo = match.group(2)

            try:
                valor = float(valor_str)
                # Tenta extrair descrição do contexto
                descricao = self._extrair_descricao_meta(texto_original, match)

                metas.append({
                    "meta": descricao or "Meta informada pelo usuário",
                    "valor_necessario": valor,
                    "prazo": prazo,
                    "confirmado": False
                })
            except ValueError:
                continue

        # Padrão alternativo: "quero comprar um carro"
        pattern2 = r"(?:quero|preciso|desejo).*?(comprar|adquirir).*?(carro|casa|apartamento|im[oó]vel)"
        match2 = re.search(pattern2, texto_lower)
        if match2:
            item = match2.group(2)
            metas.append({
                "meta": f"Comprar {item}",
                "valor_necessario": None,
                "prazo": None,
                "confirmado": False
            })

        return metas if metas else None

    def _extrair_descricao_meta(self, texto: str, match: re.Match) -> Optional[str]:
        """Extrai descrição da meta do contexto"""
        # Tenta pegar palavras antes do match
        start = max(0, match.start() - 50)
        contexto = texto[start:match.start()]

        # Procura por palavras-chave
        palavras_chave = ["casa", "apartamento", "carro", "viagem", "emergência", "reserva"]
        for palavra in palavras_chave:
            if palavra.lower() in contexto.lower():
                return f"Meta de {palavra}"

        return None

    def _extrair_idade(self, texto: str) -> Optional[int]:
        """Extrai idade"""
        patterns = [
            r"(?:tenho|idade)\s*(?:de|é)?\s*(\d+)\s*anos",
            r"idade:?\s*(\d+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                try:
                    idade = int(match.group(1))
                    return idade
                except ValueError:
                    continue

        return None

    def _extrair_profissao(self, texto: str) -> Optional[str]:
        """Extrai profissão"""
        patterns = [
            r"(?:sou|trabalho\s+como|profiss[aã]o\s+[eé])?\s*([A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜ][a-zàáâãäåèéêëìíîïòóôõöùúûü]+(?:\s+[a-zàáâãäåèéêëìíîïòóôõöùúûü]+)*)",
            r"profiss[aã]o:?\s*(.+?)(?:\.|,|$)"
        ]

        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                profissao = match.group(1).strip()
                # Filtra palavras comuns que não são profissões
                palavras_excluidas = {"João", "Maria", "Silva", "Santos", "Um", "Uma", "O", "A"}
                if profissao not in palavras_excluidas and len(profissao) > 2:
                    return profissao

        return None

    def _extrair_patrimonio(self, texto: str) -> Optional[float]:
        """Extrai patrimônio total"""
        pattern = r"(?:patrim[oô]nio).*?(\d+(?:\.\d{3})*(?:,\d{2})?)"
        match = re.search(pattern, texto)

        if match:
            valor_str = match.group(1).replace(".", "").replace(",", ".")
            try:
                return float(valor_str)
            except ValueError:
                pass

        return None

    def _extrair_reserva_emergencia(self, texto: str) -> Optional[float]:
        """Extrai valor da reserva de emergência"""
        patterns = (
            r"(?:reserva|emerg[eê]ncia).*?(\d+(?:\.\d{3})*(?:,\d{2})?)",
            r"(\d+(?:\.\d{3})*(?:,\d{2})?).*?(?:reserva|emerg[eê]ncia)",
        )
        # match = re.search(pattern, texto)
        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                valor_str = match.group(1).replace(".", "").replace(",", ".")
                try:
                    return float(valor_str)
                except ValueError:
                    pass

        return None

    def extrair_fatos_permitidos(self, usuario: Dict[str, Any]) -> Set[str]:
        """
        Extrai fatos confirmados do perfil do usuário para uso no LLM.

        Args:
            usuario: Dicionário com dados do usuário

        Returns:
            Set de fatos confirmados
        """
        if not usuario:
            return set()

        fatos = set()

        # Informações básicas (sempre incluídas)
        if usuario.get("nome"):
            fatos.add(f"Nome: {usuario['nome']}")
        if usuario.get("idade"):
            fatos.add(f"Idade: {usuario['idade']} anos")
        if usuario.get("profissao"):
            fatos.add(f"Profissão: {usuario['profissao']}")
        if usuario.get("renda_mensal"):
            fatos.add(f"Renda mensal: R$ {usuario['renda_mensal']:,.2f}")
        if usuario.get("patrimonio_total"):
            fatos.add(f"Patrimônio total: R$ {usuario['patrimonio_total']:,.2f}")
        if usuario.get("reserva_emergencia_atual"):
            fatos.add(f"Reserva de emergência: R$ {usuario['reserva_emergencia_atual']:,.2f}")

        # Perfil de investidor (apenas se confirmado)
        perfil = usuario.get("perfil_investidor", {})
        if isinstance(perfil, dict) and perfil.get("confirmado") and perfil.get("valor"):
            fatos.add(f"Perfil de investidor: {perfil['valor']}")

        # Objetivo principal (apenas se confirmado)
        objetivo = usuario.get("objetivo_principal", {})
        if isinstance(objetivo, dict) and objetivo.get("confirmado") and objetivo.get("descricao"):
            fatos.add(f"Objetivo principal: {objetivo['descricao']}")

        # Metas (apenas confirmadas)
        for meta in usuario.get("metas", []):
            if isinstance(meta, dict) and meta.get("confirmado"):
                descricao = meta.get("meta", "Meta")
                valor = meta.get("valor_necessario")
                prazo = meta.get("prazo")

                fato = f"Meta: {descricao}"
                if valor:
                    fato += f" - R$ {valor:,.2f}"
                if prazo:
                    fato += f" até {prazo}"

                fatos.add(fato)

        return fatos
