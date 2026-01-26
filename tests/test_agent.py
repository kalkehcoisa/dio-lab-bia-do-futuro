"""
Testes para o agente financeiro principal
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "app"))


class TestFinancialAgentInit:
    """Testes de inicialização do FinancialAgent"""

    def test_inicializacao(self, mock_agent):
        """Testa inicialização do agente"""
        assert mock_agent is not None
        assert mock_agent.user is not None
        assert mock_agent.data_manager is not None
        assert mock_agent.validator is not None
        assert mock_agent.llm_manager is not None

    def test_usuario_inicial_vazio(self, mock_agent):
        """Testa que usuário inicial tem estrutura padrão"""
        user = mock_agent.user
        assert "renda_mensal" in user
        assert "perfil_investidor" in user
        assert "metas" in user
        assert isinstance(user["metas"], list)


class TestWelcomeMessage:
    """Testes para mensagem de boas-vindas"""

    def test_welcome_message_existe(self, mock_agent):
        """Testa que mensagem de boas-vindas é gerada"""
        mensagem = mock_agent.welcome_message()
        assert mensagem is not None
        assert len(mensagem) > 0

    def test_welcome_message_contem_bia(self, mock_agent):
        """Testa que mensagem menciona BIA"""
        mensagem = mock_agent.welcome_message()
        assert "BIA" in mensagem

    def test_welcome_message_contem_exemplos(self, mock_agent):
        """Testa que mensagem contém exemplos de perguntas"""
        mensagem = mock_agent.welcome_message()
        assert "exemplos" in mensagem.lower() or "perguntas" in mensagem.lower()


class TestProcessMessage:
    """Testes para processamento de mensagens"""

    def test_process_message_retorna_string(self, mock_agent):
        """Testa que process_message retorna string"""
        resposta = mock_agent.process_message("olá", [])
        assert isinstance(resposta, str)
        assert len(resposta) > 0

    def test_process_message_com_historico(self, mock_agent):
        """Testa processamento com histórico"""
        history = [
            {"role": "user", "content": "oi"},
            {"role": "assistant", "content": "olá!"}
        ]
        resposta = mock_agent.process_message("como vai?", history)
        assert resposta is not None

    def test_process_message_historico_vazio(self, mock_agent):
        """Testa processamento com histórico vazio"""
        resposta = mock_agent.process_message("teste", [])
        assert resposta is not None


class TestExtractFacts:
    """Testes para extração de fatos do usuário"""

    def test_extract_facts_usuario_vazio(self, mock_agent):
        """Testa extração de fatos com usuário vazio"""
        fatos = mock_agent._extract_facts({})
        assert fatos == set()

    def test_extract_facts_com_renda(self, mock_agent, mock_usuario):
        """Testa extração de renda"""
        fatos = mock_agent._extract_facts(mock_usuario)
        assert any("Renda" in f for f in fatos)
        assert any("5" in f for f in fatos)

    def test_extract_facts_com_idade(self, mock_agent, mock_usuario):
        """Testa extração de idade"""
        fatos = mock_agent._extract_facts(mock_usuario)
        assert any("32" in f for f in fatos)

    def test_extract_facts_com_perfil_confirmado(self, mock_agent, mock_usuario):
        """Testa extração de perfil confirmado"""
        fatos = mock_agent._extract_facts(mock_usuario)
        assert any("moderado" in f.lower() for f in fatos)

    def test_extract_facts_sem_perfil_nao_confirmado(self, mock_agent):
        """Testa que perfil não confirmado não é extraído"""
        usuario = {
            "perfil_investidor": {
                "valor": "conservador",
                "confirmado": False
            }
        }
        fatos = mock_agent._extract_facts(usuario)
        assert not any("conservador" in f.lower() for f in fatos)

    def test_extract_facts_com_metas(self, mock_agent, mock_usuario):
        """Testa extração de metas"""
        fatos = mock_agent._extract_facts(mock_usuario)
        assert any("Meta" in f for f in fatos)


class TestSanitizeHistory:
    """Testes para sanitização do histórico"""

    def test_sanitize_history_remove_campos_extras(self, mock_agent):
        """Testa que campos extras são removidos"""
        history = [
            {"role": "user", "content": "oi", "extra": "campo"},
            {"role": "assistant", "content": "olá", "outro": "valor"}
        ]
        sanitized = mock_agent._sanitize_history(history)
        
        for msg in sanitized:
            assert "extra" not in msg
            assert "outro" not in msg
            assert "role" in msg
            assert "content" in msg

    def test_sanitize_history_mantem_role_content(self, mock_agent):
        """Testa que role e content são mantidos"""
        history = [{"role": "user", "content": "teste"}]
        sanitized = mock_agent._sanitize_history(history)
        
        assert sanitized[0]["role"] == "user"
        assert sanitized[0]["content"] == "teste"


class TestSquashHistory:
    """Testes para compactação do histórico"""

    def test_squash_history_pequeno_nao_compacta(self, mock_agent):
        """Testa que histórico pequeno não é compactado"""
        history = [{"role": "user", "content": f"msg{i}"} for i in range(5)]
        result = mock_agent._squash_history(history, max_messages=20)
        assert len(result) == 5

    def test_squash_history_grande_compacta(self, mock_agent):
        """Testa que histórico grande é compactado"""
        history = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg{i}"}
            for i in range(25)
        ]
        result = mock_agent._squash_history(history, max_messages=20, keep_last=6)
        assert len(result) < 25

    def test_squash_history_preserva_recentes(self, mock_agent):
        """Testa que mensagens recentes são preservadas"""
        history = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg{i}"}
            for i in range(25)
        ]
        result = mock_agent._squash_history(history, max_messages=20, keep_last=6)
        
        # Últimas 6 devem estar intactas
        assert result[-1]["content"] == "msg24"
        assert result[-6]["content"] == "msg19"


class TestMakePrompt:
    """Testes para construção do prompt"""

    def test_make_prompt_contem_system(self, mock_agent):
        """Testa que prompt contém system message"""
        messages = mock_agent._make_prompt("teste", [], set())
        assert messages[0]["role"] == "system"

    def test_make_prompt_contem_user_message(self, mock_agent):
        """Testa que prompt contém mensagem do usuário"""
        messages = mock_agent._make_prompt("minha pergunta", [], set())
        assert any(m["content"] == "minha pergunta" for m in messages)

    def test_make_prompt_com_fatos(self, mock_agent):
        """Testa que fatos são incluídos no prompt"""
        fatos = {"Renda: R$ 5000", "Idade: 30"}
        messages = mock_agent._make_prompt("teste", [], fatos)
        
        # Deve haver mensagem system com contexto
        context_msgs = [m for m in messages if "INFORMAÇÕES" in m.get("content", "")]
        assert len(context_msgs) > 0

    def test_make_prompt_inclui_historico(self, mock_agent):
        """Testa que histórico é incluído"""
        history = [
            {"role": "user", "content": "msg anterior"},
            {"role": "assistant", "content": "resposta anterior"}
        ]
        messages = mock_agent._make_prompt("nova msg", history, set())
        
        assert any("msg anterior" in m.get("content", "") for m in messages)


class TestDataExtraction:
    """Testes para extração de dados via LLM"""

    def test_extrai_renda(self, mock_agent_with_extraction):
        """Testa extração de renda da mensagem"""
        mock_agent_with_extraction.process_message("minha renda é 5000", [])
        assert mock_agent_with_extraction.user["renda_mensal"] == 5000.0

    def test_dados_persistidos(self, mock_agent_with_extraction):
        """Testa que dados são persistidos"""
        mock_agent_with_extraction.process_message("minha renda é 5000", [])
        
        # Recarrega do arquivo
        user_reloaded = mock_agent_with_extraction.data_manager.load_user()
        assert user_reloaded["renda_mensal"] == 5000.0


class TestObterResumoPerfil:
    """Testes para resumo do perfil"""

    def test_resumo_perfil_existe(self, mock_agent):
        """Testa que resumo é gerado"""
        resumo = mock_agent.obter_resumo_perfil()
        assert resumo is not None

    def test_resumo_perfil_vazio(self, mock_agent):
        """Testa resumo de perfil vazio"""
        resumo = mock_agent.obter_resumo_perfil()
        assert "Resumo" in resumo or "vazio" in resumo.lower()
