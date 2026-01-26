"""
Testes para módulo de gerenciamento de dados
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "app"))

from data import DataManager
from exceptions import DataLoadError


class TestDataManagerInit:
    """Testes de inicialização do DataManager"""

    def test_inicializacao(self, mock_data_manager):
        """Testa inicialização do DataManager"""
        assert mock_data_manager is not None
        assert mock_data_manager.user_file is not None


class TestDefaultUser:
    """Testes para usuário padrão"""

    def test_default_user_estrutura(self, mock_data_manager):
        """Testa estrutura do usuário padrão"""
        usuario = mock_data_manager.default_user()
        
        assert "renda_mensal" in usuario
        assert "perfil_investidor" in usuario
        assert "metas" in usuario
        assert isinstance(usuario["metas"], list)

    def test_default_user_valores_nulos(self, mock_data_manager):
        """Testa que valores iniciais são nulos"""
        usuario = mock_data_manager.default_user()
        
        assert usuario["renda_mensal"] is None
        assert usuario["idade"] is None
        assert usuario["profissao"] is None


class TestLoadUser:
    """Testes para carregamento de usuário"""

    def test_load_user_arquivo_nao_existe(self, mock_data_manager):
        """Testa carregamento quando arquivo não existe"""
        usuario = mock_data_manager.load_user()
        
        assert usuario is not None
        assert usuario["renda_mensal"] is None
        assert mock_data_manager.user_file.exists()

    def test_load_user_json_invalido(self, temp_user_file):
        """Testa erro ao carregar JSON inválido"""
        temp_user_file.parent.mkdir(exist_ok=True)
        with open(temp_user_file, "w") as f:
            f.write("{ invalid json }")
        
        dm = DataManager(user_file=temp_user_file)
        
        with pytest.raises(DataLoadError):
            dm.load_user()


class TestSaveUser:
    """Testes para salvamento de usuário"""

    def test_save_user_cria_arquivo(self, mock_data_manager, mock_usuario):
        """Testa que save_user cria arquivo"""
        mock_data_manager.save_user(mock_usuario)
        assert mock_data_manager.user_file.exists()

    def test_save_user_cria_diretorio(self, temp_dir):
        """Testa que save_user cria diretório se não existir"""
        arquivo_novo = temp_dir / "nova_pasta" / "usuario.json"
        dm = DataManager(user_file=arquivo_novo)
        
        usuario = dm.default_user()
        dm.save_user(usuario)
        
        assert arquivo_novo.exists()

    def test_save_user_atualiza_timestamp(self, mock_data_manager, mock_usuario_basico):
        """Testa que timestamp é atualizado ao salvar"""
        mock_usuario_basico["ultima_atualizacao"] = None
        
        mock_data_manager.save_user(mock_usuario_basico)
        usuario_carregado = mock_data_manager.load_user()
        
        assert usuario_carregado["ultima_atualizacao"] is not None


class TestSaveAndLoad:
    """Testes de salvamento e carregamento"""

    def test_salvar_e_carregar(self, mock_data_manager, mock_usuario):
        """Testa ciclo completo de salvar e carregar"""
        mock_data_manager.save_user(mock_usuario)
        usuario_carregado = mock_data_manager.load_user()
        
        assert usuario_carregado["nome"] == "João Silva"
        assert usuario_carregado["renda_mensal"] == 5000.00


class TestUpdateUser:
    """Testes para atualização de usuário"""

    def test_update_user_renda(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de renda"""
        extracted = {"renda_mensal": 6500.00}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["renda_mensal"] == 6500.00

    def test_update_user_idade(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de idade"""
        extracted = {"idade": 35}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["idade"] == 35

    def test_update_user_profissao(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de profissão"""
        extracted = {"profissao": "Engenheiro"}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["profissao"] == "Engenheiro"

    def test_update_user_perfil(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de perfil"""
        extracted = {"perfil_investidor": "moderado"}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["perfil_investidor"] == "moderado"

    def test_update_user_patrimonio(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de patrimônio"""
        extracted = {"patrimonio_total": 50000.00}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["patrimonio_total"] == 50000.00

    def test_update_user_reserva(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de reserva"""
        extracted = {"reserva_emergencia_atual": 15000.00}
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert usuario["reserva_emergencia_atual"] == 15000.00

    def test_update_user_ignora_null(self, mock_data_manager, mock_usuario):
        """Testa que valores null são ignorados"""
        renda_original = mock_usuario["renda_mensal"]
        extracted = {"renda_mensal": None, "idade": 40}
        usuario = mock_data_manager.update_user(mock_usuario, extracted)
        
        assert usuario["renda_mensal"] == renda_original
        assert usuario["idade"] == 40

    def test_update_user_metas_nova(self, mock_data_manager, mock_usuario_basico):
        """Testa adição de nova meta"""
        extracted = {
            "metas": [{
                "meta": "Comprar carro",
                "valor_necessario": 30000.00,
                "prazo": "2025-12"
            }]
        }
        usuario = mock_data_manager.update_user(mock_usuario_basico, extracted)
        
        assert len(usuario["metas"]) == 1
        assert usuario["metas"][0]["meta"] == "Comprar carro"

    def test_update_user_metas_duplicada(self, mock_data_manager, mock_usuario):
        """Testa que meta duplicada atualiza existente"""
        metas_antes = len(mock_usuario["metas"])
        extracted = {
            "metas": [{
                "meta": "Completar reserva de emergência",
                "valor_necessario": 20000.00,
                "prazo": "2026-12"
            }]
        }
        usuario = mock_data_manager.update_user(mock_usuario, extracted)
        
        # Não deve duplicar
        assert len(usuario["metas"]) == metas_antes
        # Deve atualizar valores
        meta = next(m for m in usuario["metas"] if "reserva" in m["meta"].lower())
        assert meta["valor_necessario"] == 20000.00


class TestResumoUsuario:
    """Testes para resumo do usuário"""

    def test_resumo_usuario_vazio(self, mock_data_manager):
        """Testa resumo de usuário vazio"""
        resumo = mock_data_manager.resumo_usuario(None)
        assert "vazio" in resumo.lower()

    def test_resumo_usuario_completo(self, mock_data_manager, mock_usuario):
        """Testa resumo de usuário completo"""
        resumo = mock_data_manager.resumo_usuario(mock_usuario)
        
        assert "João Silva" in resumo
        assert "Resumo" in resumo

    def test_resumo_usuario_parcial(self, mock_data_manager, mock_usuario_basico):
        """Testa resumo de usuário parcial"""
        mock_usuario_basico["renda_mensal"] = 4000.00
        resumo = mock_data_manager.resumo_usuario(mock_usuario_basico)
        
        assert "Resumo" in resumo


class TestSaveInteraction:
    """Testes para salvamento de interações"""

    def test_save_interaction_nao_falha(self, mock_data_manager):
        """Testa que save_interaction não levanta exceção"""
        mock_data_manager.save_interaction(
            "Teste mensagem",
            "Teste resposta",
            {"renda_mensal": 5000}
        )
        # Não deve falhar
        assert True
