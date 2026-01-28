"""
Validação de dados e respostas do agente
"""
from typing import Tuple, Optional, Dict, Any

import config
from exceptions import ValidationError


class DataValidator:
    """Validador de dados do usuário"""

    def __init__(self):
        self.termos_proibidos = config.TERMOS_PROIBIDOS
        self.campos_suportados = config.CAMPOS_SUPORTADOS
        self.perfis_validos = config.PERFIS_VALIDOS

    def validate_answer(
        self,
        novos_dados: Dict[str, Any],
        user_message: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida se os dados extraídos são seguros e válidos.

        Args:
            novos_dados: Dicionário com dados extraídos
            user_message: Mensagem original do usuário

        Returns:
            Tupla (valido, mensagem_erro)
        """
        texto = user_message.lower()

        # 1. Bloqueio por linguagem proibida (aconselhamento financeiro)
        for termo in self.termos_proibidos:
            if termo.lower() in texto:
                return (
                    False,
                    f"Não posso fazer recomendações ou indicar investimentos específicos. "
                    f"Posso apenas ajudar com informações educacionais e organização financeira."
                )

        if not novos_dados:
            return True, None

        # 2. Validação de campos permitidos
        for campo in novos_dados.keys():
            if campo not in self.campos_suportados:
                return False, f"O campo '{campo}' não pode ser processado."

        # 3. Validação específica por campo
        validacoes = [
            self._validar_renda_mensal,
            self._validar_perfil_investidor,
            self._validar_metas,
            self._validar_idade,
            self._validar_patrimonio,
            self._validar_reserva_emergencia
        ]

        for validacao in validacoes:
            valido, erro = validacao(novos_dados)
            if not valido:
                return False, erro

        return True, None

    def _validar_renda_mensal(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida renda mensal"""
        if "renda_mensal" not in dados:
            return True, None

        renda = dados["renda_mensal"]

        if not isinstance(renda, (int, float)):
            return False, "A renda mensal deve ser um valor numérico."

        if renda < config.MIN_RENDA_MENSAL:
            return False, "A renda mensal precisa ser um valor positivo."

        if renda > config.MAX_RENDA_MENSAL:
            return False, f"O valor informado parece muito alto. Por favor, verifique."

        return True, None

    def _validar_perfil_investidor(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida perfil de investidor"""
        if "perfil_investidor" not in dados:
            return True, None

        perfil = dados["perfil_investidor"]

        # Pode ser string ou dicionário
        if isinstance(perfil, dict):
            perfil = perfil.get("valor")

        if perfil not in self.perfis_validos:
            perfis_str = ", ".join(self.perfis_validos)
            return False, f"Perfil de investidor deve ser um dos: {perfis_str}"

        return True, None

    def _validar_metas(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida metas financeiras"""
        if "metas" not in dados:
            return True, None

        metas = dados["metas"]

        if not isinstance(metas, list):
            return False, "Metas devem ser uma lista."

        for i, meta in enumerate(metas, 1):
            if not isinstance(meta, dict):
                return False, f"Meta {i} está em formato inválido."

            # Valida valor se existir
            valor = meta.get("valor_necessario")
            if valor is not None:
                if not isinstance(valor, (int, float)):
                    return False, f"Valor da meta {i} deve ser numérico."

                if valor < config.MIN_META_VALOR:
                    return False, f"Valor da meta {i} deve ser positivo."

                if valor > config.MAX_META_VALOR:
                    return False, f"Valor da meta {i} parece muito alto."

            # Valida prazo se existir
            prazo = meta.get("prazo")
            if prazo is not None:
                if not self._validar_formato_prazo(prazo):
                    return False, f"Prazo da meta {i} deve estar no formato YYYY ou YYYY-MM."

        return True, None

    def _validar_formato_prazo(self, prazo: str) -> bool:
        """Valida formato de prazo (YYYY ou YYYY-MM)"""
        import re
        pattern = r"^\d{4}(-\d{2})?$"
        return bool(re.match(pattern, str(prazo)))

    def _validar_idade(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida idade"""
        if "idade" not in dados:
            return True, None

        idade = dados["idade"]

        if not isinstance(idade, int):
            return False, "A idade deve ser um número inteiro."

        if idade < 18 or idade > 100:
            return False, "A idade deve estar entre 18 e 100 anos."

        return True, None

    def _validar_patrimonio(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida patrimônio total"""
        if "patrimonio_total" not in dados:
            return True, None

        patrimonio = dados["patrimonio_total"]

        if not isinstance(patrimonio, (int, float)):
            return False, "O patrimônio deve ser um valor numérico."

        if patrimonio < 0:
            return False, "O patrimônio não pode ser negativo."

        return True, None

    def _validar_reserva_emergencia(self, dados: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Valida reserva de emergência"""
        if "reserva_emergencia_atual" not in dados:
            return True, None

        reserva = dados["reserva_emergencia_atual"]

        if not isinstance(reserva, (int, float)):
            return False, "A reserva de emergência deve ser um valor numérico."

        if reserva < 0:
            return False, "A reserva de emergência não pode ser negativa."

        return True, None

    def validar_consistencia_perfil(self, usuario: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Valida consistência dos dados do perfil.

        Args:
            usuario: Dicionário completo do usuário

        Returns:
            Tupla (valido, mensagem_erro)
        """
        # Reserva não pode ser maior que patrimônio
        reserva = usuario.get("reserva_emergencia_atual")
        patrimonio = usuario.get("patrimonio_total")

        if reserva and patrimonio and reserva > patrimonio:
            return False, "A reserva de emergência não pode ser maior que o patrimônio total."

        # Outras validações podem ser adicionadas aqui

        return True, None
