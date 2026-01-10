"""
Testes para módulo de validação
"""


class TestDataValidator:
    """Testes para DataValidator"""

    def test_validar_resposta_vazia(self, mock_validator):
        """Testa validação de resposta vazia"""
        valido, erro = mock_validator.validar_resposta({}, "teste")
        assert valido is True
        assert erro is None

    def test_validar_renda_valida(self, mock_validator):
        """Testa validação de renda válida"""
        dados = {"renda_mensal": 5000.00}
        valido, erro = mock_validator.validar_resposta(dados, "minha renda é 5000")

        assert valido is True
        assert erro is None

    def test_validar_renda_negativa(self, mock_validator):
        """Testa validação de renda negativa"""
        dados = {"renda_mensal": -1000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False
        assert erro is not None
        assert "positivo" in erro.lower()

    def test_validar_renda_zero(self, mock_validator):
        """Testa validação de renda zero"""
        dados = {"renda_mensal": 0}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_renda_muito_alta(self, mock_validator):
        """Testa validação de renda muito alta"""
        dados = {"renda_mensal": 2_000_000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False
        assert "alto" in erro.lower()

    def test_validar_renda_tipo_invalido(self, mock_validator):
        """Testa validação de renda com tipo inválido"""
        dados = {"renda_mensal": "abc"}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_perfil_conservador(self, mock_validator):
        """Testa validação de perfil conservador"""
        dados = {"perfil_investidor": "conservador"}
        valido, erro = mock_validator.validar_resposta(dados, "sou conservador")

        assert valido is True

    def test_validar_perfil_moderado(self, mock_validator):
        """Testa validação de perfil moderado"""
        dados = {"perfil_investidor": "moderado"}
        valido, erro = mock_validator.validar_resposta(dados, "sou moderado")

        assert valido is True

    def test_validar_perfil_arrojado(self, mock_validator):
        """Testa validação de perfil arrojado"""
        dados = {"perfil_investidor": "arrojado"}
        valido, erro = mock_validator.validar_resposta(dados, "sou arrojado")

        assert valido is True

    def test_validar_perfil_invalido(self, mock_validator):
        """Testa validação de perfil inválido"""
        dados = {"perfil_investidor": "agressivo"}
        valido, erro = mock_validator.validar_resposta(dados, "sou agressivo")

        assert valido is False
        assert "perfil" in erro.lower()

    def test_validar_perfil_dict(self, mock_validator):
        """Testa validação de perfil em formato dicionário"""
        dados = {
            "perfil_investidor": {
                "valor": "moderado",
                "confirmado": True
            }
        }
        valido, erro = mock_validator.validar_resposta(dados, "sou moderado")

        assert valido is True

    def test_validar_meta_valida(self, mock_validator):
        """Testa validação de meta válida"""
        dados = {
            "metas": [{
                "meta": "Comprar carro",
                "valor_necessario": 30000.00,
                "prazo": "2025"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "meta de comprar carro")

        assert valido is True

    def test_validar_meta_valor_negativo(self, mock_validator):
        """Testa validação de meta com valor negativo"""
        dados = {
            "metas": [{
                "meta": "Teste",
                "valor_necessario": -5000.00,
                "prazo": "2025"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_meta_valor_muito_alto(self, mock_validator):
        """Testa validação de meta com valor muito alto"""
        dados = {
            "metas": [{
                "meta": "Teste",
                "valor_necessario": 200_000_000.00,
                "prazo": "2025"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_meta_prazo_valido_ano(self, mock_validator):
        """Testa validação de meta com prazo em formato ano"""
        dados = {
            "metas": [{
                "meta": "Teste",
                "valor_necessario": 10000.00,
                "prazo": "2025"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_meta_prazo_valido_ano_mes(self, mock_validator):
        """Testa validação de meta com prazo em formato ano-mês"""
        dados = {
            "metas": [{
                "meta": "Teste",
                "valor_necessario": 10000.00,
                "prazo": "2025-06"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_meta_prazo_invalido(self, mock_validator):
        """Testa validação de meta com prazo inválido"""
        dados = {
            "metas": [{
                "meta": "Teste",
                "valor_necessario": 10000.00,
                "prazo": "proximo ano"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False
        assert "prazo" in erro.lower()

    def test_validar_meta_sem_valor(self, mock_validator):
        """Testa validação de meta sem valor"""
        dados = {
            "metas": [{
                "meta": "Comprar carro",
                "valor_necessario": None,
                "prazo": "2025"
            }]
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_meta_tipo_invalido(self, mock_validator):
        """Testa validação de metas com tipo inválido"""
        dados = {"metas": "meta invalida"}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_idade_valida(self, mock_validator):
        """Testa validação de idade válida"""
        dados = {"idade": 30}
        valido, erro = mock_validator.validar_resposta(dados, "tenho 30 anos")

        assert valido is True

    def test_validar_idade_minima(self, mock_validator):
        """Testa validação de idade mínima"""
        dados = {"idade": 18}
        valido, erro = mock_validator.validar_resposta(dados, "tenho 18 anos")

        assert valido is True

    def test_validar_idade_abaixo_minimo(self, mock_validator):
        """Testa validação de idade abaixo do mínimo"""
        dados = {"idade": 15}
        valido, erro = mock_validator.validar_resposta(dados, "tenho 15 anos")

        assert valido is False

    def test_validar_idade_acima_maximo(self, mock_validator):
        """Testa validação de idade acima do máximo"""
        dados = {"idade": 150}
        valido, erro = mock_validator.validar_resposta(dados, "tenho 150 anos")

        assert valido is False

    def test_validar_idade_tipo_invalido(self, mock_validator):
        """Testa validação de idade com tipo inválido"""
        dados = {"idade": "trinta"}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_patrimonio_valido(self, mock_validator):
        """Testa validação de patrimônio válido"""
        dados = {"patrimonio_total": 50000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_patrimonio_zero(self, mock_validator):
        """Testa validação de patrimônio zero"""
        dados = {"patrimonio_total": 0.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_patrimonio_negativo(self, mock_validator):
        """Testa validação de patrimônio negativo"""
        dados = {"patrimonio_total": -10000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_validar_reserva_valida(self, mock_validator):
        """Testa validação de reserva válida"""
        dados = {"reserva_emergencia_atual": 20000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True

    def test_validar_reserva_negativa(self, mock_validator):
        """Testa validação de reserva negativa"""
        dados = {"reserva_emergencia_atual": -5000.00}
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is False

    def test_bloquear_termo_proibido_invista(self, mock_validator):
        """Testa bloqueio de termo proibido 'invista'"""
        dados = {"renda_mensal": 5000}
        valido, erro = mock_validator.validar_resposta(dados, "invista em bitcoin")

        assert valido is False
        assert "recomend" in erro.lower()

    def test_bloquear_termo_proibido_compre(self, mock_validator):
        """Testa bloqueio de termo proibido 'compre'"""
        dados = {"renda_mensal": 5000}
        valido, erro = mock_validator.validar_resposta(dados, "compre ações agora")

        assert valido is False

    def test_bloquear_termo_proibido_recomendo(self, mock_validator):
        """Testa bloqueio de termo proibido 'recomendo'"""
        dados = {"renda_mensal": 5000}
        valido, erro = mock_validator.validar_resposta(dados, "recomendo esse investimento")

        assert valido is False

    def test_validar_consistencia_reserva_maior_patrimonio(self, mock_validator):
        """Testa validação de consistência: reserva > patrimônio"""
        usuario = {
            "patrimonio_total": 10000.00,
            "reserva_emergencia_atual": 15000.00
        }
        valido, erro = mock_validator.validar_consistencia_perfil(usuario)

        assert valido is False
        assert "reserva" in erro.lower()

    def test_validar_consistencia_valida(self, mock_validator):
        """Testa validação de consistência válida"""
        usuario = {
            "patrimonio_total": 20000.00,
            "reserva_emergencia_atual": 10000.00
        }
        valido, erro = mock_validator.validar_consistencia_perfil(usuario)

        assert valido is True

    def test_validar_multiplos_dados(self, mock_validator):
        """Testa validação de múltiplos dados"""
        dados = {
            "renda_mensal": 6000.00,
            "perfil_investidor": "moderado",
            "idade": 35
        }
        valido, erro = mock_validator.validar_resposta(dados, "teste")

        assert valido is True
