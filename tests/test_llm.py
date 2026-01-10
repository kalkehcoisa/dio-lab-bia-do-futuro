"""
Testes para módulo LLM
"""
import pytest

from app.llm import LLMManager, MockLLMProvider, OllamaProvider
from app.exceptions import LLMError


class TestMockLLMProvider:
    """Testes para MockLLMProvider"""

    def test_gerar_resposta(self):
        """Testa geração de resposta mockada"""
        provider = MockLLMProvider(response="Teste resposta")
        resposta = provider.gerar_resposta("prompt teste")

        assert resposta == "Teste resposta"
        assert provider.last_prompt == "prompt teste"

    def test_armazena_ultimo_prompt(self):
        """Testa que último prompt é armazenado"""
        provider = MockLLMProvider()
        provider.gerar_resposta("primeiro")
        provider.gerar_resposta("segundo")

        assert provider.last_prompt == "segundo"


class TestLLMManager:
    """Testes para LLMManager"""

    def test_inicializacao_com_provider(self):
        """Testa inicialização com provider customizado"""
        provider = MockLLMProvider("Teste")
        manager = LLMManager(provider=provider)

        assert manager.provider == provider

    def test_gerar_resposta_com_fatos(self, mock_llm_manager):
        """Testa geração de resposta com fatos"""
        fatos = {"Renda: R$ 5000", "Perfil: moderado"}
        resposta = mock_llm_manager.gerar_resposta("qual minha renda?", fatos)

        assert resposta is not None
        assert len(resposta) > 0

    def test_gerar_resposta_sem_fatos(self, mock_llm_manager):
        """Testa geração de resposta sem fatos"""
        resposta = mock_llm_manager.gerar_resposta("olá", set())

        assert resposta is not None

    def test_construir_prompt_com_fatos(self, mock_llm_manager):
        """Testa construção de prompt com fatos"""
        fatos = {"Renda: R$ 5000", "Idade: 30"}
        prompt = mock_llm_manager._construir_prompt("teste", fatos)

        assert "Renda: R$ 5000" in prompt
        assert "Idade: 30" in prompt
        assert "teste" in prompt
        assert "NÃO pode" in prompt

    def test_construir_prompt_sem_fatos(self, mock_llm_manager):
        """Testa construção de prompt sem fatos"""
        prompt = mock_llm_manager._construir_prompt("teste", set())

        assert "Nenhuma informação" in prompt
        assert "teste" in prompt

    def test_resposta_padrao(self, mock_llm_manager):
        """Testa resposta padrão"""
        resposta = mock_llm_manager._resposta_padrao()

        assert "Desculpe" in resposta or "dificuldade" in resposta

    def test_gerar_boas_vindas_com_nome(self, mock_llm_manager):
        """Testa geração de boas-vindas com nome"""
        mensagem = mock_llm_manager.gerar_resposta_boas_vindas("João")

        assert "João" in mensagem
        assert "BIA" in mensagem

    def test_gerar_boas_vindas_sem_nome(self, mock_llm_manager):
        """Testa geração de boas-vindas sem nome"""
        mensagem = mock_llm_manager.gerar_resposta_boas_vindas()

        assert "BIA" in mensagem
        assert "assistente" in mensagem.lower()

    def test_gerar_resposta_vazia_retorna_padrao(self, mock_llm_provider, mock_llm_manager):
        """Testa que resposta vazia retorna resposta padrão"""
        mock_llm_provider.response = ""
        resposta = mock_llm_manager.gerar_resposta("teste", set())

        assert len(resposta) > 0
        assert "Desculpe" in resposta or "dificuldade" in resposta

    def test_prompt_contem_regras(self, mock_llm_manager):
        """Testa que prompt contém regras importantes"""
        prompt = mock_llm_manager._construir_prompt("teste", set())

        assert "NÃO pode" in prompt
        assert "recomendações" in prompt or "investimento" in prompt
        assert "APENAS" in prompt

    def test_prompt_contem_contexto_usuario(self, mock_llm_manager):
        """Testa que prompt contém contexto do usuário"""
        fatos = {"Nome: João", "Renda: 5000"}
        prompt = mock_llm_manager._construir_prompt("teste", fatos)

        assert "João" in prompt
        assert "5000" in prompt


class TestOllamaProvider:
    """Testes para OllamaProvider"""

    def test_inicializacao_default(self):
        """Testa inicialização com valores padrão"""
        provider = OllamaProvider()

        assert provider.model is not None
        assert provider.timeout > 0

    def test_inicializacao_custom(self):
        """Testa inicialização com valores customizados"""
        provider = OllamaProvider(model="llama2", timeout=60)

        assert provider.model == "llama2"
        assert provider.timeout == 60

    @pytest.mark.skipif(True, reason="Requer Ollama instalado")
    def test_gerar_resposta_ollama_real(self):
        """Testa geração real com Ollama (skip se não disponível)"""
        provider = OllamaProvider()
        resposta = provider.gerar_resposta("Olá")

        assert resposta is not None
        assert len(resposta) > 0
