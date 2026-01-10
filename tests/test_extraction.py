"""
Testes para módulo de extração de dados
"""

class TestDataExtractor:
    """Testes para DataExtractor"""

    def test_extrair_renda_formato_simples(self, mock_extractor):
        """Testa extração de renda em formato simples"""
        texto = "minha renda mensal é 5000 reais"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" in dados
        assert dados["renda_mensal"] == 5000.0

    def test_extrair_renda_formato_milhar(self, mock_extractor):
        """Testa extração de renda com separador de milhar"""
        texto = "meu salário é de 8.500 reais"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" in dados
        assert dados["renda_mensal"] == 8500.0

    def test_extrair_renda_formato_decimal(self, mock_extractor):
        """Testa extração de renda com decimal"""
        texto = "ganho 3500,50 por mês"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" in dados
        assert dados["renda_mensal"] == 3500.50

    def test_extrair_renda_com_rs(self, mock_extractor):
        """Testa extração de renda com símbolo R$"""
        texto = "minha renda é R$ 7.200"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" in dados
        assert dados["renda_mensal"] == 7200.0

    def test_extrair_perfil_conservador(self, mock_extractor):
        """Testa extração de perfil conservador"""
        texto = "meu perfil é conservador"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "perfil_investidor" in dados
        assert dados["perfil_investidor"] == "conservador"

    def test_extrair_perfil_moderado(self, mock_extractor):
        """Testa extração de perfil moderado"""
        texto = "sou moderado como investidor"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "perfil_investidor" in dados
        assert dados["perfil_investidor"] == "moderado"

    def test_extrair_perfil_arrojado(self, mock_extractor):
        """Testa extração de perfil arrojado"""
        texto = "me considero arrojado"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "perfil_investidor" in dados
        assert dados["perfil_investidor"] == "arrojado"

    def test_extrair_meta_completa(self, mock_extractor):
        """Testa extração de meta com valor e prazo"""
        texto = "minha meta é juntar 50000 até 2026"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "metas" in dados
        assert len(dados["metas"]) == 1
        assert dados["metas"][0]["valor_necessario"] == 50000.0
        assert dados["metas"][0]["prazo"] == "2026"

    def test_extrair_meta_economizar(self, mock_extractor):
        """Testa extração de meta com verbo economizar"""
        texto = "preciso economizar 20000 para 2025"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "metas" in dados
        assert dados["metas"][0]["valor_necessario"] == 20000.0

    def test_extrair_meta_guardar(self, mock_extractor):
        """Testa extração de meta com verbo guardar"""
        texto = "quero guardar 15000 até 2027"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "metas" in dados
        assert dados["metas"][0]["valor_necessario"] == 15000.0

    def test_extrair_meta_comprar_carro(self, mock_extractor):
        """Testa extração de meta de comprar carro"""
        texto = "quero comprar um carro novo"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "metas" in dados
        assert "carro" in dados["metas"][0]["meta"].lower()

    def test_extrair_meta_comprar_casa(self, mock_extractor):
        """Testa extração de meta de comprar casa"""
        texto = "preciso comprar uma casa"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "metas" in dados
        assert "casa" in dados["metas"][0]["meta"].lower()

    def test_extrair_idade(self, mock_extractor):
        """Testa extração de idade"""
        texto = "tenho 35 anos"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "idade" in dados
        assert dados["idade"] == 35

    def test_extrair_idade_formato_alternativo(self, mock_extractor):
        """Testa extração de idade em formato alternativo"""
        texto = "idade: 42"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "idade" in dados
        assert dados["idade"] == 42

    def test_extrair_profissao(self, mock_extractor):
        """Testa extração de profissão"""
        texto = "sou Engenheiro de Software"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "profissao" in dados
        assert "Engenheiro" in dados["profissao"]

    def test_extrair_patrimonio(self, mock_extractor):
        """Testa extração de patrimônio"""
        texto = "meu patrimônio total é 100000"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "patrimonio_total" in dados
        assert dados["patrimonio_total"] == 100000.0

    def test_extrair_reserva_emergencia(self, mock_extractor):
        """Testa extração de reserva de emergência"""
        texto = "tenho 25000 na reserva de emergência"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "reserva_emergencia_atual" in dados
        assert dados["reserva_emergencia_atual"] == 25000.0

    def test_extrair_multiplos_dados(self, mock_extractor):
        """Testa extração de múltiplos dados na mesma mensagem"""
        texto = "tenho 30 anos, ganho 6000 por mês e sou moderado"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "idade" in dados
        assert "renda_mensal" in dados
        assert "perfil_investidor" in dados
        assert dados["idade"] == 30
        assert dados["renda_mensal"] == 6000.0
        assert dados["perfil_investidor"] == "moderado"

    def test_detectar_dados_texto_vazio(self, mock_extractor):
        """Testa extração com texto vazio"""
        dados = mock_extractor.detectar_novos_dados("")
        assert dados == {}

    def test_detectar_dados_texto_irrelevante(self, mock_extractor):
        """Testa extração com texto irrelevante"""
        texto = "olá, como vai você?"
        dados = mock_extractor.detectar_novos_dados(texto)
        assert dados == {}

    def test_extrair_fatos_permitidos_vazio(self, mock_extractor):
        """Testa extração de fatos de usuário vazio"""
        fatos = mock_extractor.extrair_fatos_permitidos({})
        assert isinstance(fatos, set)
        assert len(fatos) == 0

    def test_extrair_fatos_permitidos_completo(self, mock_extractor, mock_usuario):
        """Testa extração de fatos de usuário completo"""
        fatos = mock_extractor.extrair_fatos_permitidos(mock_usuario)

        assert isinstance(fatos, set)
        assert len(fatos) > 0
        assert any("João Silva" in fato for fato in fatos)
        assert any("5,000" in fato for fato in fatos)
        assert any("moderado" in fato for fato in fatos)

    def test_extrair_fatos_apenas_confirmados(self, mock_extractor, mock_usuario):
        """Testa que apenas dados confirmados são extraídos"""
        # Adiciona meta não confirmada
        mock_usuario["metas"].append({
            "meta": "Meta não confirmada",
            "valor_necessario": 10000.0,
            "confirmado": False
        })

        fatos = mock_extractor.extrair_fatos_permitidos(mock_usuario)
        fatos_str = " ".join(fatos)

        # Meta confirmada deve estar
        assert "Completar reserva" in fatos_str
        # Meta não confirmada não deve estar
        assert "Meta não confirmada" not in fatos_str

    def test_extrair_idade_invalida(self, mock_extractor):
        """Testa que idade inválida é extraída"""
        texto = "tenho 200 anos"
        dados = mock_extractor.detectar_novos_dados(texto)

        # deve extrair idade acima de 150
        assert "idade" in dados

    def test_extrair_renda_valor_invalido(self, mock_extractor):
        """Testa que valor inválido de renda não é extraído"""
        texto = "minha renda é abc reais"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" not in dados

    def test_extrair_perfil_inexistente(self, mock_extractor):
        """Testa que perfil inexistente não é extraído"""
        texto = "sou ultra arrojado"
        dados = mock_extractor.detectar_novos_dados(texto)

        # "ultra arrojado" não é um perfil válido
        assert "perfil_investidor" not in dados or dados["perfil_investidor"] == "arrojado"

    def test_case_insensitive(self, mock_extractor):
        """Testa que extração é case-insensitive"""
        texto = "MINHA RENDA É 5000 REAIS E SOU CONSERVADOR"
        dados = mock_extractor.detectar_novos_dados(texto)

        assert "renda_mensal" in dados
        assert "perfil_investidor" in dados
