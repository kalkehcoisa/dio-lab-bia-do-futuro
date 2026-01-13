"""
Integração com Large Language Model
"""

from typing import Set, Optional

from groq import Groq, GroqError

import config
from exceptions import LLMError


class LLMProvider:
    """Interface para provedores de LLM"""
    def gerar_resposta(self, prompt: str) -> str:
        """Gera resposta baseada no prompt fornecido"""
        raise NotImplementedError


class GroqProvider(LLMProvider):
    def __init__(self, model=config.GROQ_MODEL_NAME):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = model

    def gerar_resposta(self, prompt: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=config.GROQ_LLM_TIMEOUT,
            )
            response = resp.choices[0].message.content.strip()
            return response

        except GroqError as e:
            if "rate limit" in str(e).lower():
                raise LLMError("Rate limit atingido.")
            elif "authentication" in str(e).lower():
                raise LLMError("API key inválida.")
            else:
                raise LLMError(f"Erro Groq: {e}")


class LLMManager:
    """Gerenciador de interações com LLM"""

    def __init__(self, provider: LLMProvider = GroqProvider()):
        self.provider = provider

    def gerar_resposta(
        self,
        mensagem_usuario: str,
        fatos_permitidos: Set[str]
    ) -> str:
        """
        Gera resposta baseada em fatos permitidos.

        Args:
            mensagem_usuario: Mensagem do usuário
            fatos_permitidos: Set de fatos confirmados

        Returns:
            Resposta gerada pelo LLM

        Raises:
            LLMError: Se houver erro na geração
        """
        prompt = self._construir_prompt(mensagem_usuario, fatos_permitidos)
        resposta = self.provider.gerar_resposta(prompt)

        # Validação básica da resposta
        if not resposta or len(resposta.strip()) == 0:
            return self._resposta_padrao()

        return resposta

    def _construir_prompt(
        self,
        mensagem: str,
        fatos: Set[str]
    ) -> str:
        """Constrói prompt estruturado para o LLM"""
        contexto = "\n".join(f"- {f}" for f in fatos if f)

        if not contexto:
            contexto = "- Nenhuma informação disponível ainda"

        prompt = f"""Você é BIA, uma assistente financeira educacional amigável e profissional.

REGRAS IMPORTANTES:
1. Você NÃO pode fazer recomendações de investimento específicos
2. Você NÃO pode indicar produtos financeiros específicos
3. Você DEVE usar APENAS os fatos fornecidos abaixo
4. Se não tiver informação suficiente, diga claramente
5. Seja educativa, não prescritiva
6. Mantenha tom amigável e profissional

INFORMAÇÕES DISPONÍVEIS DO USUÁRIO:
{contexto}

PERGUNTA DO USUÁRIO:
{mensagem}

INSTRUÇÕES:
- Responda de forma clara e objetiva
- Use apenas as informações disponíveis acima
- Se precisar de mais informações, pergunte ao usuário
- Não invente dados ou faça suposições
- Seja útil mas não dê conselhos de investimento específicos
- Sempre que apresentar um resultado, descreva como ele foi obtido (fórmulas, metodologias, etc)

Responda agora:"""

        return prompt

    def _resposta_padrao(self) -> str:
        """Retorna resposta padrão em caso de erro"""
        return (
            "Desculpe, tive dificuldade em processar sua mensagem. "
            "Pode reformular de outra forma?"
        )

    def gerar_resposta_boas_vindas(self, nome: Optional[str] = None) -> str:
        """Gera mensagem de boas-vindas personalizada"""
        if nome:
            return f"""Olá, {nome}!

Sou a BIA, sua assistente financeira pessoal. Estou aqui para ajudar você a:

Organizar suas informações financeiras
Acompanhar suas metas
Entender melhor seu perfil financeiro
Aprender sobre educação financeira

Como posso ajudar você hoje?"""
        else:
            return """Olá!

Sou a BIA, sua assistente financeira pessoal.

Para começar, que tal me contar um pouco sobre você?
Por exemplo: sua renda mensal, seu perfil de investidor (conservador, moderado ou arrojado),
ou suas metas financeiras.

Como posso ajudar você hoje?"""
