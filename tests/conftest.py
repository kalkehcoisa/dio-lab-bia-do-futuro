"""
Configurações e fixtures para testes
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def temp_dir():
    """Cria diretório temporário para testes"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_usuario_file(temp_dir):
    """Cria arquivo temporário para usuário"""
    data_path = temp_dir / "data"
    data_path.mkdir()
    return data_path / "usuario.json"


@pytest.fixture
def mock_data_manager(temp_usuario_file):
    """Fixture para DataManager com arquivo temporário"""
    from app.data import DataManager
    return DataManager(usuario_file=temp_usuario_file)


@pytest.fixture
def mock_extractor():
    """Fixture para DataExtractor"""
    from app.extraction import DataExtractor
    return DataExtractor()


@pytest.fixture
def mock_validator():
    """Fixture para DataValidator"""
    from app.validation import DataValidator
    return DataValidator()


@pytest.fixture
def mock_llm_provider():
    """Fixture para provider LLM mockado"""
    from app.llm import MockLLMProvider
    return MockLLMProvider(response="Resposta de teste")


@pytest.fixture
def mock_llm_manager(mock_llm_provider):
    """Fixture para LLMManager com provider mockado"""
    from app.llm import LLMManager
    return LLMManager(provider=mock_llm_provider)


@pytest.fixture
def mock_agent(mock_data_manager, mock_extractor, mock_validator, mock_llm_manager):
    """Fixture para FinancialAgent completo"""
    from app.agent import FinancialAgent
    agent = FinancialAgent(
        data_manager=mock_data_manager,
        extractor=mock_extractor,
        validator=mock_validator,
        llm_manager=mock_llm_manager
    )
    agent.inicializar()
    return agent


@pytest.fixture
def mock_agent_malandro(mock_data_manager, mock_extractor, mock_validator):
    """Fixture para FinancialAgent completo"""
    from app.agent import FinancialAgent
    from app.llm import LLMManager, MockLLMProvider

    response = ' '.join([
        "invista em bitcoin",
        "recomendo comprar ações",
        "aplique em tesouro direto",
        "compre fundos imobiliários"
    ])

    mock_llm_provider = MockLLMProvider(response=response)
    agent = FinancialAgent(
        data_manager=mock_data_manager,
        extractor=mock_extractor,
        validator=mock_validator,
        llm_manager=LLMManager(provider=mock_llm_provider)
    )
    agent.inicializar()
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
