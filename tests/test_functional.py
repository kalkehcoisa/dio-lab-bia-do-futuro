"""
Testes funcionais (integração) do agente financeiro
"""
import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "app"))
sys.path.insert(0, str(Path(__file__).parent))

from tests.conftest import MockLLMProvider, MockLLMManager


class TestFluxoBasico:
    """Testes de fluxo básico do agente"""

    def test_boas_vindas(self, mock_agent):
        """Testa mensagem de boas-vindas"""
        mensagem = mock_agent.welcome_message()
        
        assert len(mensagem) > 0
        assert "BIA" in mensagem

    def test_processar_mensagem_simples(self, mock_agent):
        """Testa processamento de mensagem simples"""
        resposta = mock_agent.process_message("olá", [])
        
        assert resposta is not None
        assert len(resposta) > 0

    def test_resumo_perfil(self, mock_agent):
        """Testa obtenção de resumo"""
        resumo = mock_agent.obter_resumo_perfil()
        
        assert resumo is not None


class TestExtracaoDados:
    """Testes de extração de dados"""

    def test_extrai_renda(self, mock_data_manager, mock_validator):
        """Testa extração de renda"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Entendi! Sua renda é R$ 6.000,00.",
            "user_message": "minha renda é 6000",
            "dados_extraidos": {
                "renda_mensal": 6000.0,
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
        
        agent.process_message("minha renda é 6000", [])
        assert agent.user["renda_mensal"] == 6000.0

    def test_extrai_idade(self, mock_data_manager, mock_validator):
        """Testa extração de idade"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Entendi! Você tem 30 anos.",
            "user_message": "tenho 30 anos",
            "dados_extraidos": {
                "renda_mensal": None,
                "perfil_investidor": None,
                "idade": 30,
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
        
        agent.process_message("tenho 30 anos", [])
        assert agent.user["idade"] == 30

    def test_extrai_perfil(self, mock_data_manager, mock_validator):
        """Testa extração de perfil"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Entendi! Seu perfil é moderado.",
            "user_message": "sou moderado",
            "dados_extraidos": {
                "renda_mensal": None,
                "perfil_investidor": "moderado",
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
        
        agent.process_message("sou moderado", [])
        assert agent.user["perfil_investidor"] == "moderado"

    def test_extrai_multiplos_dados(self, mock_data_manager, mock_validator):
        """Testa extração de múltiplos dados"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Entendi! Você tem 35 anos e ganha R$ 7.000.",
            "user_message": "tenho 35 anos e ganho 7000",
            "dados_extraidos": {
                "renda_mensal": 7000.0,
                "perfil_investidor": None,
                "idade": 35,
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
        
        agent.process_message("tenho 35 anos e ganho 7000", [])
        assert agent.user["idade"] == 35
        assert agent.user["renda_mensal"] == 7000.0


class TestPersistencia:
    """Testes de persistência de dados"""

    def test_dados_persistidos(self, mock_data_manager, mock_validator):
        """Testa que dados são persistidos"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Renda salva!",
            "user_message": "renda 5500",
            "dados_extraidos": {
                "renda_mensal": 5500.0,
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
        
        agent.process_message("minha renda é 5500", [])
        
        # Recarrega do arquivo
        user_reloaded = mock_data_manager.load_user()
        assert user_reloaded["renda_mensal"] == 5500.0

    def test_persistencia_entre_sessoes(self, temp_user_file, mock_validator):
        """Testa persistência entre sessões"""
        from agent import FinancialAgent
        from data import DataManager
        
        provider = MockLLMProvider(response_data={
            "resposta": "Renda salva!",
            "user_message": "renda 8000",
            "dados_extraidos": {
                "renda_mensal": 8000.0,
                "perfil_investidor": None,
                "idade": None,
                "profissao": None,
                "patrimonio_total": None,
                "reserva_emergencia_atual": None,
                "metas": None
            }
        })
        
        # Sessão 1
        dm1 = DataManager(user_file=temp_user_file)
        agent1 = FinancialAgent(
            data_manager=dm1,
            validator=mock_validator,
            llm_manager=MockLLMManager(provider=provider)
        )
        agent1.process_message("minha renda é 8000", [])
        assert agent1.user["renda_mensal"] == 8000.0
        
        # Sessão 2
        dm2 = DataManager(user_file=temp_user_file)
        agent2 = FinancialAgent(
            data_manager=dm2,
            validator=mock_validator,
            llm_manager=MockLLMManager(provider=MockLLMProvider())
        )
        
        # Dados devem ter sido carregados
        assert agent2.user["renda_mensal"] == 8000.0


class TestContexto:
    """Testes de uso de contexto"""

    def test_fatos_no_prompt(self, mock_data_manager, mock_validator, mock_usuario):
        """Testa que fatos do usuário vão para o prompt"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider()
        
        agent = FinancialAgent(
            data_manager=mock_data_manager,
            validator=mock_validator,
            llm_manager=MockLLMManager(provider=provider)
        )
        
        # Configura usuário com dados
        agent.user = mock_usuario
        
        # Processa mensagem
        agent.process_message("qual minha renda?", [])
        
        # Verifica que prompt contém dados do usuário
        last_prompt = provider.last_prompt
        prompt_text = json.dumps(last_prompt)
        
        assert "5" in prompt_text  # renda 5000
        assert "moderado" in prompt_text.lower()

    def test_historico_incluso(self, mock_agent):
        """Testa que histórico é incluído"""
        history = [
            {"role": "user", "content": "pergunta anterior"},
            {"role": "assistant", "content": "resposta anterior"}
        ]
        
        mock_agent.process_message("nova pergunta", history)
        
        last_prompt = mock_agent.llm_manager.provider.last_prompt
        prompt_text = json.dumps(last_prompt)
        
        assert "pergunta anterior" in prompt_text


class TestRobustez:
    """Testes de robustez"""

    def test_mensagem_vazia(self, mock_agent):
        """Testa processamento de mensagem vazia"""
        resposta = mock_agent.process_message("", [])
        assert resposta is not None

    def test_historico_vazio(self, mock_agent):
        """Testa processamento com histórico vazio"""
        resposta = mock_agent.process_message("teste", [])
        assert resposta is not None

    def test_historico_com_campos_extras(self, mock_agent):
        """Testa que campos extras no histórico são ignorados"""
        history = [
            {"role": "user", "content": "oi", "extra": "campo", "outro": 123}
        ]
        resposta = mock_agent.process_message("teste", history)
        assert resposta is not None

    def test_dados_nulos_ignorados(self, mock_data_manager, mock_validator):
        """Testa que dados nulos são ignorados"""
        from agent import FinancialAgent
        
        provider = MockLLMProvider(response_data={
            "resposta": "Olá!",
            "user_message": "oi",
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
        
        agent = FinancialAgent(
            data_manager=mock_data_manager,
            validator=mock_validator,
            llm_manager=MockLLMManager(provider=provider)
        )
        
        # Define renda inicial
        agent.user["renda_mensal"] = 5000.0
        
        # Processa mensagem que não extrai dados
        agent.process_message("oi", [])
        
        # Renda não deve ser sobrescrita
        assert agent.user["renda_mensal"] == 5000.0
