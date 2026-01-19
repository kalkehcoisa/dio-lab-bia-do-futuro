"""
Lógica principal do agente financeiro
"""
from typing import Dict, Any, Tuple, Optional

from data import DataManager
from validation import DataValidator
from llm import LLMManager
from exceptions import AgentException


HISTORY_ALLOWED_KEYS = {"role", "content"}

SYSTEM_PROMPT = """
Você é BIA, uma assistente financeira educacional amigável e profissional.

REGRAS IMPORTANTES:
1. Você NÃO pode fazer recomendações de investimento específicos
2. Você NÃO pode indicar produtos financeiros específicos
3. Você DEVE usar APENAS os fatos fornecidos abaixo
4. Se não tiver informação suficiente, diga claramente
5. Seja educativa, não prescritiva
6. Mantenha tom amigável e profissional

INSTRUÇÕES:
- Responda de forma clara e objetiva
- Use apenas as informações disponíveis acima
- Se precisar de mais informações, pergunte ao usuário
- Não invente dados ou faça suposições
- Seja útil mas não dê conselhos de investimento específicos
- Sempre que apresentar um resultado, descreva como ele foi obtido (fórmulas, metodologias, etc)

Você DEVE responder SEMPRE em JSON válido.
Nunca escreva texto fora do JSON.

A chave "resposta" é o espaço para sua usual. 

Formato obrigatório:
{
  "resposta": string,
  "user_message": string,
  "dados_extraidos": {
    "renda_mensal": number | null,
    "perfil_investidor": string | null,
    "idade": number | null,
    "profissao": string | null,
    "patrimonio_total": number | null,
    "reserva_emergencia_atual": number | null,
    "metas": [
      {
        "meta": string,
        "valor_necessario": number | null,
        "prazo": string | null
      }
    ] | null
  }
}

Use null quando a informação não estiver clara.
Não invente valores.
"""

INSTRUCTIONS = 'INFORMAÇÕES DISPONÍVEIS DO USUÁRIO:\n{context}'


class FinancialAgent:
    """Agente Financeiro Inteligente"""

    def __init__(
        self,
        data_manager: Optional[DataManager] = None,
        validator: Optional[DataValidator] = None,
        llm_manager: Optional[LLMManager] = None
    ):
        """
        Inicializa o agente financeiro.

        Args:
            data_manager: Gerenciador de dados
            validator: Validador de dados
            llm_manager: Gerenciador de LLM
        """
        self.data_manager = data_manager or DataManager()
        self.validator = validator or DataValidator()
        self.llm_manager = llm_manager or LLMManager()

        self.user = self.data_manager.load_user()

    def _sanitize_history(self, history: list[dict]):
        return [
            {k: v for k, v in msg.items() if k in HISTORY_ALLOWED_KEYS}
            for msg in history
            if isinstance(msg, dict)
        ]

    def _make_prompt(
        self,
        user_message: str,
        history: list[dict],
        facts: set[str]
    ) -> list[dict]:
        """Constrói prompt estruturado para o LLM"""
        context = "\n".join(f"- {f}" for f in facts if f)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_message},
        ]
        if context:
            messages.insert(1, {
                "role": "system",
                "content": INSTRUCTIONS.format(context=context)
            })

        return messages

    def _squash_history(
            self,
            history: list[dict],
            max_messages: int = 20,
            keep_last: int = 6
    ) -> list[dict]:
        """
        Compacta o histórico de conversa quando ultrapassa um limite definido.

        Estratégia:
        - Mantém as últimas `keep_last` mensagens intactas
        - Junta (concatena) mensagens antigas do usuário e do assistente
        - Substitui mensagens antigas por blocos compactados
        - Preserva o formato compatível com ChatInterface / OpenAI / Groq

        Args:
            history (list[dict]): Histórico de mensagens no formato
                {"role": "user" | "assistant", "content": str}
            max_messages (int): Quantidade máxima de mensagens antes da compactação
            keep_last (int): Quantidade de mensagens recentes a preservar sem compactar

        Returns:
            list[dict]: Histórico compactado, pronto para envio ao LLM
        """
        if len(history) <= max_messages:
            return history

        older_messages = history[:-keep_last]
        recent_messages = history[-keep_last:]

        user_contents = []
        assistant_contents = []

        for message in older_messages:
            role = message.get("role")
            content = message.get("content")

            if not content:
                continue

            if role == "user":
                user_contents.append(content)
            elif role == "assistant":
                assistant_contents.append(content)

        compacted = []

        if user_contents:
            compacted.append({
                "role": "user",
                "content": (
                    "Resumo de mensagens anteriores do usuário:\n"
                    + "\n".join(user_contents)
                ),
            })

        if assistant_contents:
            compacted.append({
                "role": "assistant",
                "content": (
                    "Resumo de respostas anteriores do assistente:\n"
                    + "\n".join(assistant_contents)
                ),
            })

        return compacted + recent_messages

    def _extract_facts(self, usuario: dict[str, Any]) -> set[str]:
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

    def process_message(
            self,
            user_message: str,
            history: list[dict]
        ) -> str:
        """
        Processa mensagem do usuário e retorna resposta.

        Args:
            user_message: Mensagem do usuário

        Returns:
            Tupla (resposta, dados_atualizados)

        Raises:
            AgentException: Se houver erro no processamento
        """
        try:
            history = self._sanitize_history(history)
            history = self._squash_history(history)
            facts = self._extract_facts(self.user)
            messages_prompt = self._make_prompt(
                user_message=user_message,
                history=history,
                facts=facts
            )
            llm_answer = self.llm_manager.generate_answer(
                messages_prompt=messages_prompt
            )
            self.data_manager.save_interaction(
                user_message=user_message,
                answer=llm_answer['resposta'],
                extracted_data=llm_answer['dados_extraidos'],
            )
            self.user = self.data_manager.update_user(
                user=self.user,
                extracted_data=llm_answer['dados_extraidos']
            )
            self.data_manager.save_user(user=self.user)

            return llm_answer['resposta']
        except AgentException:
            raise
        except Exception as e:
            # em produção seria melhor tratar os erros e fazer logs
            raise

    def welcome_message(self) -> str:
        """Retorna mensagem de boas-vindas"""
        nome = self.user.get("nome") if self.user else None
        return f"Olá, {nome}!" if nome else "Olá!" + """

Sou a BIA, sua assistente financeira pessoal. Estou aqui para ajudar você a:

Organizar suas informações financeiras
Acompanhar suas metas
Entender melhor seu perfil financeiro
Aprender sobre educação financeira

Como posso ajudar você hoje?"""

    def obter_resumo_perfil(self) -> str:
        """Retorna resumo do perfil do usuário"""
        return self.data_manager.resumo_usuario(self.user)
