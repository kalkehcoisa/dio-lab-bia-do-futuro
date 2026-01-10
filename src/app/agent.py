"""
Lógica principal do agente financeiro
"""
from typing import Dict, Any, Tuple, Optional, List

from .config import PALAVRAS_CONFIRMACAO, PALAVRAS_NEGACAO
from .data import DataManager
from .extraction import DataExtractor
from .validation import DataValidator
from .llm import LLMManager
from .exceptions import AgentException


class FinancialAgent:
    """Agente Financeiro Inteligente"""

    def __init__(
        self,
        data_manager: Optional[DataManager] = None,
        extractor: Optional[DataExtractor] = None,
        validator: Optional[DataValidator] = None,
        llm_manager: Optional[LLMManager] = None
    ):
        """
        Inicializa o agente financeiro.

        Args:
            data_manager: Gerenciador de dados
            extractor: Extrator de dados
            validator: Validador de dados
            llm_manager: Gerenciador de LLM
        """
        self.data_manager = data_manager or DataManager()
        self.extractor = extractor or DataExtractor()
        self.validator = validator or DataValidator()
        self.llm_manager = llm_manager or LLMManager()

        self.usuario = None
        self.pendente_confirmacao = None

    def inicializar(self) -> Dict[str, Any]:
        """
        Inicializa o agente e carrega dados do usuário.

        Returns:
            Dados do usuário carregados
        """
        self.usuario = self.data_manager.carregar_usuario()
        return self.usuario

    def eh_confirmacao(self, texto: str) -> bool:
        """
        Verifica se o texto é uma confirmação.

        Args:
            texto: Texto a verificar

        Returns:
            True se for confirmação
        """
        texto_lower = texto.lower().strip()
        return any(palavra in texto_lower for palavra in PALAVRAS_CONFIRMACAO)

    def eh_negacao(self, texto: str) -> bool:
        """
        Verifica se o texto é uma negação.

        Args:
            texto: Texto a verificar

        Returns:
            True se for negação
        """
        texto_lower = texto.lower().strip()
        return any(palavra in texto_lower for palavra in PALAVRAS_NEGACAO)

    def formatar_confirmacao(self, dados: Dict[str, Any]) -> str:
        """
        Formata mensagem de confirmação de dados.

        Args:
            dados: Dicionário com dados a confirmar

        Returns:
            Mensagem formatada
        """
        linhas = ["Identifiquei as seguintes informações:\n"]

        for chave, valor in dados.items():
            if chave == "renda_mensal":
                linhas.append(f"**Renda Mensal**: R$ {valor:,.2f}")
            elif chave == "perfil_investidor":
                perfil = valor if isinstance(valor, str) else valor.get("valor", valor)
                linhas.append(f"**Perfil de Investidor**: {perfil.title()}")
            elif chave == "metas":
                linhas.append(f"\n**Novas Metas**:")
                if isinstance(valor, list):
                    for i, meta in enumerate(valor, 1):
                        desc = meta.get("meta", "Meta")
                        val = meta.get("valor_necessario")
                        prazo = meta.get("prazo")

                        linha_meta = f"  {i}. {desc}"
                        if val:
                            linha_meta += f" - R$ {val:,.2f}"
                        if prazo:
                            linha_meta += f" (até {prazo})"
                        linhas.append(linha_meta)
            elif chave == "idade":
                linhas.append(f"**Idade**: {valor} anos")
            elif chave == "profissao":
                linhas.append(f"**Profissão**: {valor}")
            elif chave == "patrimonio_total":
                linhas.append(f"**Patrimônio Total**: R$ {valor:,.2f}")
            elif chave == "reserva_emergencia_atual":
                linhas.append(f"**Reserva de Emergência**: R$ {valor:,.2f}")
            else:
                linhas.append(f"- **{chave}**: {valor}")

        linhas.append("\n**Posso salvar essas informações?** (responda sim ou não)")
        return "\n".join(linhas)

    def processar_mensagem(self, mensagem: str) -> Tuple[str, Dict[str, Any]]:
        """
        Processa mensagem do usuário e retorna resposta.

        Args:
            mensagem: Mensagem do usuário

        Returns:
            Tupla (resposta, dados_atualizados)

        Raises:
            AgentException: Se houver erro no processamento
        """
        try:
            # 1. Se há confirmação pendente
            if self.pendente_confirmacao:
                return self._processar_confirmacao(mensagem)

            # 2. Detectar novos dados
            novos_dados = self.extractor.detectar_novos_dados(mensagem)

            if novos_dados:
                ok, resp_erro = self.validator.validar_resposta(novos_dados, mensagem)
                if not ok:
                    return resp_erro, novos_dados
                return self._processar_novos_dados(mensagem, novos_dados)

            # 3. Apenas conversa (sem persistência)
            return self._processar_conversa(mensagem)

        except AgentException:
            raise
        except Exception as e:
            raise AgentException(f"Erro ao processar mensagem: {e}")

    def _processar_confirmacao(self, mensagem: str) -> Tuple[str, Dict[str, Any]]:
        """Processa resposta a pedido de confirmação"""
        if self.eh_confirmacao(mensagem):
            # Confirma e salva dados
            novos_dados = self.pendente_confirmacao
            self.usuario = self.data_manager.aplicar_atualizacoes(
                self.usuario,
                novos_dados
            )

            # Valida consistência do perfil completo
            valido, erro = self.validator.validar_consistencia_perfil(self.usuario)
            if not valido:
                # Reverte alterações
                self.usuario = self.data_manager.carregar_usuario()
                self.pendente_confirmacao = None
                return erro, self.usuario

            self.data_manager.salvar_usuario(self.usuario)
            self.data_manager.salvar_interacao(
                mensagem,
                "Dados confirmados",
                novos_dados
            )

            self.pendente_confirmacao = None

            resposta = (
                "✅ **Dados confirmados e salvos com sucesso!**\n\n" +
                self.data_manager.resumo_usuario(self.usuario)
            )
            return resposta, self.usuario

        elif self.eh_negacao(mensagem):
            # Cancela operação
            self.pendente_confirmacao = None
            return "Ok, não salvei nenhuma informação. Como posso ajudar?", self.usuario
        else:
            # Resposta ambígua
            return (
                "Não entendi. Você confirma essas informações? "
                "Por favor, responda **sim** ou **não**."
            ), self.usuario

    def _processar_novos_dados(
        self,
        mensagem: str,
        novos_dados: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Processa novos dados extraídos"""
        # Valida dados extraídos
        valido, erro = self.validator.validar_resposta(novos_dados, mensagem)

        if not valido:
            self.data_manager.salvar_interacao(mensagem, erro, novos_dados)
            return erro, self.usuario

        # Solicita confirmação
        self.pendente_confirmacao = novos_dados
        resposta = self.formatar_confirmacao(novos_dados)

        self.data_manager.salvar_interacao(
            mensagem,
            "Aguardando confirmação",
            novos_dados
        )

        return resposta, self.usuario

    def _processar_conversa(self, mensagem: str) -> Tuple[str, Dict[str, Any]]:
        """Processa conversa normal sem extração de dados"""
        try:
            fatos = self.extractor.extrair_fatos_permitidos(self.usuario)
            resposta_llm = self.llm_manager.gerar_resposta(mensagem, fatos)
            ok, resp_erro = self.validator.validar_resposta({}, resposta_llm)
            if not ok:
                return resp_erro, self.usuario

            self.data_manager.salvar_interacao(mensagem, resposta_llm)

            return resposta_llm, self.usuario

        except Exception as e:
            # Em caso de erro no LLM, retorna resposta padrão
            resposta = (
                "Desculpe, tive dificuldade em processar sua mensagem. "
                "Pode reformular de outra forma?"
            )
            return resposta, self.usuario

    def obter_mensagem_boas_vindas(self) -> str:
        """Retorna mensagem de boas-vindas"""
        nome = self.usuario.get("nome") if self.usuario else None
        return self.llm_manager.gerar_resposta_boas_vindas(nome)

    def obter_resumo_perfil(self) -> str:
        """Retorna resumo do perfil do usuário"""
        return self.data_manager.resumo_usuario(self.usuario)

    def resetar_confirmacao_pendente(self) -> None:
        """Reseta confirmação pendente"""
        self.pendente_confirmacao = None

    def tem_confirmacao_pendente(self) -> bool:
        """Verifica se há confirmação pendente"""
        return self.pendente_confirmacao is not None
