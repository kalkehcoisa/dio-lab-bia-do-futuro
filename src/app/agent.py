"""
Lógica principal do agente financeiro
"""
from typing import Any, Optional

from data import DataManager
from validation import DataValidator
from llm import LLMManager
from exceptions import AgentException


HISTORY_ALLOWED_KEYS = {"role", "content"}

FORMAT_PROMPT = """
Você DEVE responder SEMPRE em JSON válido.
Nunca escreva texto fora do JSON.

Formato obrigatório:
{
  "resposta": string,
  "user_message": string,
  "dados_extraidos": {
    "nome": string | null,
    "renda_mensal": number | null,
    "perfil_investidor": string | null,
    "idade": number | null,
    "profissao": string | null,
    "patrimonio_total": number | null,
    "reserva_emergencia_atual": number | null,
    "objetivo_principal": string | null,
    "aceita_risco": boolean | null,
    "metas": [
      {
        "meta": string,
        "valor_necessario": number | null,
        "prazo": string | null
      }
    ] | null
  }
}
Importante: jamais responda em formato diferente do JSON acima.
NUNCA ADICIONE TEXTO FORA DO JSON.
"""

SYSTEM_PROMPT = """
Você é BIA, uma assistente financeira educacional amigável e profissional.

REGRAS IMPORTANTES:
1. Você NÃO pode fazer recomendações de investimento específicos
2. Você NÃO pode indicar produtos financeiros específicos
3. Você DEVE usar APENAS os fatos fornecidos abaixo
4. Se não tiver informação suficiente, diga claramente
5. Seja educativa, não prescritiva
6. Mantenha tom amigável e profissional

COMPORTAMENTO PROATIVO - COLETA DE INFORMAÇÕES:
Você deve ser proativa na coleta de informações do usuário. A cada interação, verifique quais informações ainda faltam e tente coletar de forma natural e amigável.

Informações essenciais que você DEVE coletar (em ordem de prioridade):
1. nome - Pergunte logo no início se ainda não souber
2. idade - Importante para adequar orientações
3. profissao - Ajuda a entender contexto financeiro
4. renda_mensal - Fundamental para qualquer orientação
5. patrimonio_total - Para entender situação atual
6. reserva_emergencia_atual - Para avaliar segurança financeira
7. objetivo_principal - O que o usuário quer alcançar
8. perfil_investidor - Conservador, moderado ou arrojado
9. aceita_risco - Se está disposto a correr riscos
10. metas - Objetivos específicos com valores e prazos

ESTRATÉGIA DE COLETA:
- Ao final de CADA resposta, se houver informações faltando, faça UMA pergunta para coletar um dado que ainda não tenha
- Seja natural: "A propósito, você poderia me dizer sua idade? Isso me ajuda a dar orientações mais adequadas para sua fase de vida."
- Explique brevemente por que precisa da informação
- Não bombardeie com muitas perguntas de uma vez

SUGESTÕES PROATIVAS:
Ao final de suas respostas, quando apropriado, sugira:
- Perguntas que o usuário poderia fazer: "Você gostaria de saber sobre...?"
- Tópicos relacionados ao que foi discutido
- Próximos passos no planejamento financeiro
- Simulações úteis baseadas nas informações que você já tem

Exemplos de sugestões:
- "💡 Com sua renda, posso calcular quanto você deveria ter de reserva de emergência. Quer que eu faça essa simulação?"
- "📊 Podemos conversar sobre como organizar seu orçamento mensal. O que acha?"
- "🎯 Você mencionou que quer comprar um carro. Quer que eu calcule quanto precisaria poupar por mês?"

INSTRUÇÕES:
- Responda de forma clara e objetiva
- Use apenas as informações disponíveis acima
- Se precisar de mais informações, pergunte ao usuário
- Não invente dados ou faça suposições
- Seja útil mas não dê conselhos de investimento específicos

SIMULAÇÕES FINANCEIRAS:
Você pode fazer cálculos financeiros quando solicitado. Exemplos:
- Parcelamento com/sem juros (use fórmula Price se houver juros)
- Comparação à vista vs parcelado
- Projeção de reserva de emergência
- Juros compostos

Ao fazer cálculos, mostre:
1. O resultado principal em destaque
2. Os valores usados no cálculo
3. Uma breve explicação do raciocínio

Use null quando a informação não estiver clara.
Não invente valores.

VALIDAÇÃO DE DADOS:
Retorne null para dados claramente irreais ou inválidos:
- idade: deve estar entre 0 e 100 anos
- renda_mensal: deve ser um valor positivo
- patrimonio_total: deve ser um valor não negativo
- reserva_emergencia_atual: deve ser um valor não negativo
- metas.valor_necessario: deve ser um valor positivo
Se o usuário informar dados fora desses limites, não extraia o valor (use null).
"""

INSTRUCTIONS = 'INFORMAÇÕES DISPONÍVEIS DO USUÁRIO:\n{context}'

EXAMPLES = """
Consigo parcelar uma compra de R$ 3.000?
Vale mais pagar à vista ou parcelar?
Como funcionam os juros do cartão de crédito?
Quais investimentos existem para quem ganha um salário mínimo?
"""

SQUASH_INSTRUCTIONS ="""
Você é um assistente que resume conversas.
Resuma a conversa abaixo de forma concisa, mantendo os pontos principais
e informações relevantes sobre o usuário. Responda apenas com o resumo.

Responda em formato JSON:
{
    "resposta": string,
}
"""


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
            {"role": "system", "content": FORMAT_PROMPT},
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
            max_messages: int = 5,
            keep_last: int = 2
    ) -> list[dict]:
        """
        Compacta o histórico de conversa quando ultrapassa um limite definido.

        Estratégia:
        - Mantém as últimas `keep_last` mensagens intactas
        - Envia mensagens antigas ao LLM para gerar um resumo
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

        conversation_text = self._format_messages_as_text(older_messages)

        summary_prompt = [
            {
                "role": "system",
                "content": SQUASH_INSTRUCTIONS,
            },
            {
                "role": "user",
                "content": f"Resuma esta conversa:\n\n{conversation_text}"
            }
        ]

        summary = self.llm_manager.generate_answer(summary_prompt)

        compacted = [
            {
                "role": "system",
                "content": f"Resumo da conversa anterior:\n{summary}"
            }
        ]

        return compacted + recent_messages

    def _format_messages_as_text(self, messages: list[dict]) -> str:
        """Converte lista de mensagens em texto legível."""
        lines = []
        for message in messages:
            role = message.get("role", "unknown")
            content = message.get("content")

            if not content:
                continue

            if isinstance(content, list):
                text_parts = [
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict) and item.get("type") == "text"
                ]
                text = " ".join(text_parts).strip()
            else:
                text = str(content).strip()

            if text:
                role_label = "Usuário" if role == "user" else "Assistente"
                lines.append(f"{role_label}: {text}")

        return "\n".join(lines)

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
            if 'dados_extraidos' in llm_answer:
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
        global EXAMPLES
        nome = self.user.get("nome") if self.user else None
        
        if nome:
            greeting = f"Olá, {nome}! Que bom ver você de novo! 😊"
        else:
            greeting = "Olá! Sou a BIA, sua assistente financeira pessoal. 😊"
        
        missing_info = self._get_missing_info_prompt()
        
        return f"""{greeting}

Estou aqui para ajudar você a:
📊 Organizar suas informações financeiras
🎯 Acompanhar suas metas
💡 Entender melhor seu perfil financeiro
📚 Aprender sobre educação financeira

Alguns exemplos do que posso fazer:
{EXAMPLES}
{missing_info}
Como posso ajudar você hoje?"""

    def _get_missing_info_prompt(self) -> str:
        """Retorna uma sugestão para coletar informação faltante"""
        if not self.user:
            return "\n🤝 Para começar, que tal me contar seu nome?\n"
        
        if not self.user.get("nome"):
            return "\n🤝 Para começar, que tal me contar seu nome?\n"
        if not self.user.get("idade"):
            return "\n💬 Me conta, qual a sua idade? Isso me ajuda a dar orientações mais adequadas.\n"
        if not self.user.get("profissao"):
            return "\n💼 Qual é a sua profissão? Conhecer sua área de atuação me ajuda a entender melhor seu contexto.\n"
        if not self.user.get("renda_mensal"):
            return "\n💰 Qual é sua renda mensal aproximada? Com essa informação, posso fazer simulações mais precisas.\n"
        if not self.user.get("objetivo_principal", {}).get("descricao"):
            return "\n🎯 Qual seu principal objetivo financeiro no momento?\n"
        
        return ""

    def obter_resumo_perfil(self) -> str:
        """Retorna resumo do perfil do usuário"""
        return self.data_manager.resumo_usuario(self.user)
