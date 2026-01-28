"""
Integração com Large Language Model
"""

import json

from groq import Groq, GroqError

import config
from exceptions import LLMError


class GroqProvider:
    def __init__(self, model=config.GROQ_MODEL_NAME):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = model

    def generate_answer(self, messages_propmt: list[dict]) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages_propmt,
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

    def __init__(self, provider=None):
        if provider is None:
            provider = GroqProvider()
        self.provider = provider

    def generate_answer(
        self,
        messages_prompt: list[dict]
    ) -> dict:
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
        answer = self.provider.generate_answer(messages_prompt)
        print("start:\n", answer, "\nend")
        try:
            json_answer = json.loads(answer)
        except json.JSONDecodeError:
            try:
                response, json_answer = answer.split('\n{')
                json_answer = json.loads(json_answer)
                json_answer['resposta'] = response
            except ValueError:
                raise LLMError(
                "Erro ao se comunicar com o servidor. Por favor, aguarde e tente novamente mais tarde."
            )
        # Validação básica da resposta
        if not json_answer['resposta'] or len(json_answer['resposta'].strip()) == 0:
            json_answer['resposta'] = self._default_answer()

        return json_answer

    def _default_answer(self) -> str:
        """Retorna resposta padrão em caso de erro"""
        return (
            "Desculpe, tive dificuldade em processar sua mensagem. "
            "Poderia escrever de outra forma?"
        )
