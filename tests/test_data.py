"""
Testes para módulo de gerenciamento de dados
"""
import pytest

from app.data import DataManager
from app.exceptions import DataLoadError


class TestDataManager:
    """Testes para DataManager"""

    def test_usuario_padrao(self, mock_data_manager):
        """Testa criação de usuário padrão"""
        usuario = mock_data_manager.usuario_padrao()

        assert usuario is not None
        assert "renda_mensal" in usuario
        assert "perfil_investidor" in usuario
        assert "metas" in usuario
        assert isinstance(usuario["metas"], list)

    def test_load_user_arquivo_nao_existe(self, mock_data_manager):
        """Testa carregamento quando arquivo não existe"""
        usuario = mock_data_manager.load_user()

        assert usuario is not None
        assert usuario["renda_mensal"] is None
        # Verifica que arquivo foi criado
        assert mock_data_manager.user_file.exists()

    def test_salvar_e_load_user(self, mock_data_manager, mock_usuario):
        """Testa salvar e carregar usuário"""
        # Salva
        mock_data_manager.save_user(mock_usuario)
        assert mock_data_manager.user_file.exists()

        # Carrega
        usuario_carregado = mock_data_manager.load_user()
        assert usuario_carregado["nome"] == "João Silva"
        assert usuario_carregado["renda_mensal"] == 5000.00
        assert "ultima_atualizacao" in usuario_carregado

    def test_save_user_cria_diretorio(self, temp_dir):
        """Testa que salvar cria diretório se não existir"""
        arquivo_novo = temp_dir / "nova_pasta" / "usuario.json"
        dm = DataManager(user_file=arquivo_novo)

        usuario = dm.usuario_padrao()
        dm.save_user(usuario)

        assert arquivo_novo.exists()
        assert arquivo_novo.parent.exists()

    def test_update_user_data_renda(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de renda mensal"""
        updates = {"renda_mensal": 6500.00}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["renda_mensal"] == 6500.00

    def test_update_user_data_perfil_string(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de perfil com string"""
        updates = {"perfil_investidor": "arrojado"}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["perfil_investidor"]["valor"] == "arrojado"
        assert usuario_atualizado["perfil_investidor"]["confirmado"] is True

    def test_update_user_data_perfil_dict(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de perfil com dicionário"""
        updates = {
            "perfil_investidor": {
                "valor": "conservador",
                "confirmado": True
            }
        }
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["perfil_investidor"]["valor"] == "conservador"

    def test_update_user_data_metas(self, mock_data_manager, mock_usuario_basico):
        """Testa adição de metas"""
        updates = {
            "metas": [{
                "meta": "Comprar carro",
                "valor_necessario": 30000.00,
                "prazo": "2025-12"
            }]
        }
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert len(usuario_atualizado["metas"]) == 1
        assert usuario_atualizado["metas"][0]["meta"] == "Comprar carro"
        assert usuario_atualizado["metas"][0]["confirmado"] is True

    def test_update_user_data_multiplas_metas(self, mock_data_manager, mock_usuario):
        """Testa adição de múltiplas metas"""
        metas_iniciais = len(mock_usuario["metas"])

        updates = {
            "metas": [
                {"meta": "Viagem", "valor_necessario": 10000.00, "prazo": "2025-06"},
                {"meta": "Curso", "valor_necessario": 5000.00, "prazo": "2025-03"}
            ]
        }
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario, updates)

        assert len(usuario_atualizado["metas"]) == metas_iniciais + 2

    def test_update_user_data_idade(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de idade"""
        updates = {"idade": 35}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["idade"] == 35

    def test_update_user_data_profissao(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de profissão"""
        updates = {"profissao": "Engenheiro"}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["profissao"] == "Engenheiro"

    def test_update_user_data_patrimonio(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de patrimônio"""
        updates = {"patrimonio_total": 50000.00}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["patrimonio_total"] == 50000.00

    def test_update_user_data_reserva(self, mock_data_manager, mock_usuario_basico):
        """Testa atualização de reserva de emergência"""
        updates = {"reserva_emergencia_atual": 15000.00}
        usuario_atualizado = mock_data_manager.update_user_data(mock_usuario_basico, updates)

        assert usuario_atualizado["reserva_emergencia_atual"] == 15000.00

    def test_resumo_usuario_vazio(self, mock_data_manager):
        """Testa resumo de usuário vazio"""
        resumo = mock_data_manager.resumo_usuario(None)
        assert "vazio" in resumo.lower()

    def test_resumo_mock_usuario(self, mock_data_manager, mock_usuario):
        """Testa resumo de usuário completo"""
        resumo = mock_data_manager.resumo_usuario(mock_usuario)

        assert "João Silva" in resumo
        assert "5,000" in resumo
        assert "moderado" in resumo.lower()
        assert "meta" in resumo.lower()

    def test_resumo_usuario_parcial(self, mock_data_manager, mock_usuario_basico):
        """Testa resumo de usuário com dados parciais"""
        mock_usuario_basico["renda_mensal"] = 4000.00
        resumo = mock_data_manager.resumo_usuario(mock_usuario_basico)

        assert "4,000" in resumo
        assert "Resumo" in resumo

    def test_load_user_json_invalido(self, temp_user_file):
        """Testa erro ao carregar JSON inválido"""
        temp_user_file.parent.mkdir(exist_ok=True)
        with open(temp_user_file, "w") as f:
            f.write("{ invalid json }")

        dm = DataManager(user_file=temp_user_file)

        with pytest.raises(DataLoadError):
            dm.load_user()

    def test_save_interaction(self, mock_data_manager, temp_dir):
        """Testa salvamento de interação"""
        # Mock do path de interações
        interacoes_path = temp_dir / "data" / "interacoes"
        interacoes_path.mkdir(parents=True, exist_ok=True)

        # Salva interação (não deve falhar)
        mock_data_manager.save_interaction(
            "Teste mensagem",
            "Teste resposta",
            {"renda_mensal": 5000}
        )

        # Verifica que não levantou exceção
        assert True

    def test_timestamp_atualizacao(self, mock_data_manager, mock_usuario_basico):
        """Testa que timestamp é atualizado ao salvar"""
        mock_usuario_basico["ultima_atualizacao"] = None

        mock_data_manager.save_user(mock_usuario_basico)
        usuario_carregado = mock_data_manager.load_user()

        assert usuario_carregado["ultima_atualizacao"] is not None
        assert len(usuario_carregado["ultima_atualizacao"]) > 0
