"""
Integração com Large Language Model
"""
import subprocess
from typing import Set, Optional
from abc import ABC, abstractmethod

from .config import LLM_MODEL, LLM_TIMEOUT
from .exceptions import LLMError


class LLMProvider(ABC):
    """Interface abstrata para provedores de LLM"""

    @abstractmethod
    def gerar_resposta(self, prompt: str) -> str:
        """Gera resposta a partir de um prompt"""
        pass


class OllamaProvider(LLMProvider):
    """Provedor LLM usando Ollama local"""

    def __init__(self, model: str = LLM_MODEL, timeout: int = LLM_TIMEOUT):
        self.model = model
        self.timeout = timeout

    def gerar_resposta(self, prompt: str) -> str:
        """
        Gera resposta usando Ollama.

        Args:
            prompt: Prompt para o modelo

        Returns:
            Resposta gerada

        Raises:
            LLMError: Se houver erro na geração
        """
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=self.timeout
            )

            if result.returncode != 0:
                raise LLMError(f"Erro ao executar Ollama: {result.stderr}")

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise LLMError(f"Timeout ao gerar resposta (>{self.timeout}s)")
        except FileNotFoundError:
            raise LLMError("Ollama não está instalado ou não está no PATH")
        except Exception as e:
            raise LLMError(f"Erro inesperado ao gerar resposta: {e}")


class MockLLMProvider(LLMProvider):
    """Provedor mock para testes"""

    def __init__(self, response: str = "Resposta mockada"):
        self.response = response
        self.last_prompt = None

    def gerar_resposta(self, prompt: str) -> str:
        """Retorna resposta mockada"""
        self.last_prompt = prompt
        return self.response


class LLMManager:
    """Gerenciador de interações com LLM"""

    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or OllamaProvider()

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

        try:
            resposta = self.provider.gerar_resposta(prompt)

            # Validação básica da resposta
            if not resposta or len(resposta.strip()) == 0:
                return self._resposta_padrao()

            return resposta

        except LLMError:
            raise
        except Exception as e:
            raise LLMError(f"Erro ao gerar resposta: {e}")

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
