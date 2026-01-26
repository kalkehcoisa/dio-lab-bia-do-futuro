"""
Configurações e fixtures para testes
"""
import pytest
import tempfile
import shutil
import json
from pathlib import Path
from typing import Dict, Any
import sys

# Adiciona src/app ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "app"))


class MockLLMProvider:
    """Provedor mock para testes - simula resposta do LLM"""

    def __init__(self, response_data: dict = None):
        self.response_data = response_data or {
            "resposta": "Resposta mockada do assistente.",
            "user_message": "mensagem do usuário",
            "dados_extraidos": {
                "renda_mensal": None,
                "perfil_investidor": None,
                "idade": None,
                "profissao": None,
                "patrimonio_total": None,
                "reserva_emergencia_atual": None,
                "metas": None
            }
        }
        self.last_prompt = None

    def generate_answer(self, messages_prompt: list[dict]) -> str:
        """Retorna resposta mockada em JSON"""
        self.last_prompt = messages_prompt
        return json.dumps(self.response_data, ensure_ascii=False)


class MockLLMManager:
    """LLMManager mockado para testes"""

    def __init__(self, provider: MockLLMProvider = None):
        self.provider = provider or MockLLMProvider()

    def generate_answer(self, messages_prompt: list[dict]) -> dict:
        """Retorna resposta parseada"""
        response = self.provider.generate_answer(messages_prompt)
        return json.loads(response)


@pytest.fixture
def temp_dir():
    """Cria diretório temporário para testes"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_user_file(temp_dir):
    """Cria arquivo temporário para usuário"""
    data_path = temp_dir / "data"
    data_path.mkdir()
    interacoes_path = data_path / "interacoes"
    interacoes_path.mkdir()
    return data_path / "usuario.json"


@pytest.fixture
def mock_data_manager(temp_user_file):
    """Fixture para DataManager com arquivo temporário"""
    from data import DataManager
    return DataManager(user_file=temp_user_file)


@pytest.fixture
def mock_validator():
    """Fixture para DataValidator"""
    from validation import DataValidator
    return DataValidator()


@pytest.fixture
def mock_llm_provider():
    """Fixture para provider LLM mockado"""
    return MockLLMProvider()


@pytest.fixture
def mock_llm_manager(mock_llm_provider):
    """Fixture para LLMManager com provider mockado"""
    return MockLLMManager(provider=mock_llm_provider)


@pytest.fixture
def mock_agent(mock_data_manager, mock_validator, mock_llm_manager):
    """Fixture para FinancialAgent completo"""
    from agent import FinancialAgent
    agent = FinancialAgent(
        data_manager=mock_data_manager,
        validator=mock_validator,
        llm_manager=mock_llm_manager
    )
    return agent


@pytest.fixture
def mock_agent_with_extraction(mock_data_manager, mock_validator):
    """Fixture para FinancialAgent que extrai renda"""
    from agent import FinancialAgent
    
    provider = MockLLMProvider(response_data={
        "resposta": "Entendi! Sua renda mensal é R$ 5.000,00.",
        "user_message": "minha renda é 5000",
        "dados_extraidos": {
            "renda_mensal": 5000.0,
            "perfil_investidor": None,
            "idade": None,
            "profissao": None,
            "patrimonio_total": None,
            "reserva_emergencia_atual": None,
            "metas": None
        }
    })
    
    agent = FinancialAgent(
        data_manager=mock_data_manager,
        validator=mock_validator,
        llm_manager=MockLLMManager(provider=provider)
    )
    return agent


@pytest.fixture
def mock_usuario() -> Dict[str, Any]:
    """Fixture com dados completos de usuário"""
    return {
        "nome": "João Silva",
        "idade": 32,
        "profissao": "Analista de Sistemas",
        "renda_mensal": 5000.00,
        "perfil_investidor": {
            "valor": "moderado",
            "confirmado": True
        },
        "objetivo_principal": {
            "descricao": "Construir reserva de emergência",
            "confirmado": True
        },
        "patrimonio_total": 15000.00,
        "reserva_emergencia_atual": 10000.00,
        "aceita_risco": False,
        "metas": [
            {
                "meta": "Completar reserva de emergência",
                "valor_necessario": 15000.00,
                "prazo": "2026-06",
                "confirmado": True
            }
        ],
        "ultima_atualizacao": "2024-01-01 10:00:00"
    }


@pytest.fixture
def mock_usuario_basico() -> Dict[str, Any]:
    """Fixture com dados básicos de usuário"""
    return {
        "nome": None,
        "idade": None,
        "profissao": None,
        "renda_mensal": None,
        "perfil_investidor": {
            "valor": None,
            "confirmado": False
        },
        "objetivo_principal": {
            "descricao": None,
            "confirmado": False
        },
        "patrimonio_total": None,
        "reserva_emergencia_atual": None,
        "aceita_risco": False,
        "metas": [],
        "ultima_atualizacao": None
    }
