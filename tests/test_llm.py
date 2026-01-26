"""
Testes para módulo LLM
"""
import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "app"))

from llm import LLMManager
from exceptions import LLMError


class MockProvider:
    """Provider mock para testes"""
    
    def __init__(self, response: str = None):
        self.response = response or json.dumps({
            "resposta": "Resposta de teste",
            "user_message": "teste",
            "dados_extraidos": {
                "renda_mensal": None,
                "perfil_investidor": None,
                "idade": None,
                "profissao": None,
                "patrimonio_total": None,
                "reserva_emergencia_atual": None,
                "metas": None
            }
        })
        self.last_prompt = None

    def generate_answer(self, messages_prompt: list[dict]) -> str:
        self.last_prompt = messages_prompt
        return self.response


class TestLLMManager:
    """Testes para LLMManager"""

    def test_inicializacao_com_provider(self):
        """Testa inicialização com provider customizado"""
        provider = MockProvider()
        manager = LLMManager(provider=provider)
        assert manager.provider == provider

    def test_generate_answer_retorna_dict(self):
        """Testa que generate_answer retorna dicionário"""
        provider = MockProvider()
        manager = LLMManager(provider=provider)
        
        messages = [{"role": "user", "content": "teste"}]
        result = manager.generate_answer(messages)
        
        assert isinstance(result, dict)
        assert "resposta" in result
        assert "dados_extraidos" in result

    def test_generate_answer_com_resposta_valida(self):
        """Testa geração com resposta válida"""
        provider = MockProvider(json.dumps({
            "resposta": "Sua renda é R$ 5.000",
            "user_message": "qual minha renda",
            "dados_extraidos": {
                "renda_mensal": 5000.0,
                "perfil_investidor": None,
                "idade": None,
                "profissao": None,
                "patrimonio_total": None,
                "reserva_emergencia_atual": None,
                "metas": None
            }
        }))
        manager = LLMManager(provider=provider)
        
        messages = [{"role": "user", "content": "qual minha renda"}]
        result = manager.generate_answer(messages)
        
        assert "5.000" in result["resposta"]
        assert result["dados_extraidos"]["renda_mensal"] == 5000.0

    def test_generate_answer_json_invalido(self):
        """Testa erro com JSON inválido"""
        provider = MockProvider("isso não é json válido")
        manager = LLMManager(provider=provider)
        
        messages = [{"role": "user", "content": "teste"}]
        
        with pytest.raises(LLMError):
            manager.generate_answer(messages)

    def test_generate_answer_resposta_vazia_usa_padrao(self):
        """Testa que resposta vazia usa padrão"""
        provider = MockProvider(json.dumps({
            "resposta": "",
            "user_message": "teste",
            "dados_extraidos": {}
        }))
        manager = LLMManager(provider=provider)
        
        messages = [{"role": "user", "content": "teste"}]
        result = manager.generate_answer(messages)
        
        assert len(result["resposta"]) > 0
        assert "Desculpe" in result["resposta"] or "dificuldade" in result["resposta"]

    def test_default_answer(self):
        """Testa resposta padrão"""
        provider = MockProvider()
        manager = LLMManager(provider=provider)
        
        resposta = manager._default_answer()
        
        assert "Desculpe" in resposta or "dificuldade" in resposta


class TestLLMManagerIntegration:
    """Testes de integração (requerem provider real)"""

    @pytest.mark.skip(reason="Requer API key configurada")
    def test_groq_provider_real(self):
        """Testa com Groq real (skip se não disponível)"""
        from llm import GroqProvider
        
        provider = GroqProvider()
        manager = LLMManager(provider=provider)
        
        messages = [
            {"role": "system", "content": "Responda em JSON"},
            {"role": "user", "content": "Olá"}
        ]
        result = manager.generate_answer(messages)
        
        assert result is not None
