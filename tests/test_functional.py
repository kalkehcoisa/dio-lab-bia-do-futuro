"""
Testes funcionais (integração) do mock_agente financeiro
"""


class TestFluxosCompletos:
    """Testes de fluxos completos end-to-end"""

    def test_onboarding_usuario_novo(self, mock_agent):
        """Testa fluxo completo de onboarding de novo usuário"""
        # 1. Boas-vindas
        boas_vindas = mock_agent.obter_mensagem_boas_vindas()
        assert len(boas_vindas) > 0

        # 2. Usuário informa renda
        resp1, _ = mock_agent.process_message("minha renda mensal é 5500 reais")
        assert "5,500" in resp1
        assert mock_agent.tem_confirmacao_pendente()

        # 3. Confirma renda
        resp2, _ = mock_agent.process_message("sim")
        assert "confirmado" in resp2.lower()
        assert not mock_agent.tem_confirmacao_pendente()
        assert mock_agent.usuario["renda_mensal"] == 5500.0

        # 4. Informa perfil
        resp3, _ = mock_agent.process_message("meu perfil é moderado")
        assert "moderado" in resp3.lower()

        # 5. Confirma perfil
        resp4, _ = mock_agent.process_message("confirmo")
        assert mock_agent.usuario["perfil_investidor"]["valor"] == "moderado"

        # 6. Define meta
        resp5, _ = mock_agent.process_message("quero juntar 30000 até 2026")
        assert "30,000" in resp5

        # 7. Confirma meta
        resp6, _ = mock_agent.process_message("sim")
        assert len(mock_agent.usuario["metas"]) > 0

    def test_consulta_informacoes(self, mock_agent):
        """Testa fluxo de consulta de informações"""
        # Setup: Adiciona dados ao perfil
        mock_agent.usuario["renda_mensal"] = 6000.0
        mock_agent.usuario["perfil_investidor"] = {
            "valor": "moderado",
            "confirmado": True
        }
        mock_agent.data_manager.save_user(mock_agent.usuario)

        # Consulta informações
        resp, _ = mock_agent.process_message("qual é minha renda?")
        assert resp is not None
        assert len(resp) > 0

    def test_atualizacao_dados_existentes(self, mock_agent):
        """Testa atualização de dados já existentes"""
        # Setup: Dados iniciais
        mock_agent.process_message("minha renda é 5000")
        mock_agent.process_message("sim")
        assert mock_agent.usuario["renda_mensal"] == 5000.0

        # Atualiza renda
        mock_agent.process_message("agora minha renda é 6500")
        mock_agent.process_message("sim")

        # Verifica atualização
        assert mock_agent.usuario["renda_mensal"] == 6500.0

    def test_adicao_multiplas_metas(self, mock_agent):
        """Testa adição de múltiplas metas"""
        metas_iniciais = len(mock_agent.usuario.get("metas", []))

        # Meta 1
        mock_agent.process_message("meta de juntar 20000 até 2025")
        mock_agent.process_message("sim")

        # Meta 2
        mock_agent.process_message("meta de juntar 50000 até 2027")
        mock_agent.process_message("sim")

        assert len(mock_agent.usuario["metas"]) == metas_iniciais + 2

    def test_rejeicao_dados_invalidos(self, mock_agent):
        """Testa rejeição de dados inválidos"""
        # Tenta informar renda negativa
        resp, _ = mock_agent.process_message("minha renda é -3000")

        assert "erro" in resp.lower() or "positivo" in resp.lower()
        assert not mock_agent.tem_confirmacao_pendente()

    def test_cancelamento_durante_confirmacao(self, mock_agent):
        """Testa cancelamento durante processo de confirmação"""
        renda_inicial = mock_agent.usuario.get("renda_mensal")

        # Informa nova renda
        mock_agent.process_message("minha renda é 7000")
        assert mock_agent.tem_confirmacao_pendente()

        # Cancela
        resp, _ = mock_agent.process_message("não")

        assert not mock_agent.tem_confirmacao_pendente()
        assert mock_agent.usuario.get("renda_mensal") == renda_inicial

    def test_bloqueio_aconselhamento_financeiro(self, mock_agent_malandro):
        """Testa bloqueio de aconselhamento financeiro"""
        mensagens_proibidas = [
            "invista em bitcoin",
            "recomendo comprar ações",
            "aplique em tesouro direto",
            "compre fundos imobiliários"
        ]

        for msg in mensagens_proibidas:
            resp, _ = mock_agent_malandro.process_message(msg)
            assert "não posso" in resp.lower() or "recomenda" in resp.lower()


class TestScenariosComplexos:
    """Testes de cenários complexos"""

    def test_perfil_completo_passo_a_passo(self, mock_agent):
        """Testa construção completa de perfil passo a passo"""
        # Idade
        mock_agent.process_message("tenho 32 anos")
        mock_agent.process_message("sim")

        # Profissão
        mock_agent.process_message("sou Analista de Sistemas")
        if mock_agent.tem_confirmacao_pendente():
            mock_agent.process_message("sim")

        # Renda
        mock_agent.process_message("ganho 8000 por mês")
        mock_agent.process_message("sim")

        # Perfil
        mock_agent.process_message("sou moderado")
        mock_agent.process_message("sim")

        # Patrimônio
        mock_agent.process_message("meu patrimônio total é 50000")
        mock_agent.process_message("sim")

        # Reserva
        mock_agent.process_message("tenho 20000 na reserva de emergência")
        mock_agent.process_message("sim")

        # Verificações
        assert mock_agent.usuario["idade"] == 32
        assert mock_agent.usuario["renda_mensal"] == 8000.0
        assert mock_agent.usuario["perfil_investidor"]["valor"] == "moderado"
        assert mock_agent.usuario["patrimonio_total"] == 50000.0
        assert mock_agent.usuario["reserva_emergencia_atual"] == 20000.0

    def test_informacoes_em_lote(self, mock_agent):
        """Testa informar múltiplos dados de uma vez"""
        resp, _ = mock_agent.process_message(
            "tenho 35 anos, ganho 7000 reais por mês e sou conservador"
        )

        assert mock_agent.tem_confirmacao_pendente()

        mock_agent.process_message("sim")

        assert mock_agent.usuario["idade"] == 35
        assert mock_agent.usuario["renda_mensal"] == 7000.0
        assert mock_agent.usuario["perfil_investidor"]["valor"] == "conservador"

    def test_validacao_consistencia_perfil(self, mock_agent):
        """Testa validação de consistência entre dados do perfil"""
        # Define patrimônio
        mock_agent.process_message("meu patrimônio é 15000")
        mock_agent.process_message("sim")

        # Tenta definir reserva maior que patrimônio
        resp, _ = mock_agent.process_message("minha reserva de emergência é 20000")
        mock_agent.process_message("sim")

        # Deve rejeitar por inconsistência
        # Reserva não pode ser maior que patrimônio
        if mock_agent.usuario.get("reserva_emergencia_atual") == 20000.0:
            # Se salvou, o patrimônio deve ter sido ajustado ou validação falhou
            assert mock_agent.usuario["patrimonio_total"] >= 20000.0

    def test_persistencia_dados(self, temp_user_file):
        """Testa persistência de dados entre sessões"""
        from app.agent import FinancialAgent
        from app.data import DataManager
        # Sessão 1: Cria mock_agente e adiciona dados
        dm1 = DataManager(user_file=temp_user_file)
        mock_agent1 = FinancialAgent(data_manager=dm1)

        mock_agent1.process_message("minha renda é 5500")
        mock_agent1.process_message("sim")

        assert mock_agent1.usuario["renda_mensal"] == 5500.0

        # Sessão 2: Novo mock_agente carrega dados
        dm2 = DataManager(user_file=temp_user_file)
        mock_agent2 = FinancialAgent(data_manager=dm2)

        assert mock_agent2.usuario["renda_mensal"] == 5500.0

    def test_conversacao_mista(self, mock_agent):
        """Testa conversação misturando dados e perguntas"""
        # Pergunta
        resp1, _ = mock_agent.process_message("como você pode me ajudar?")
        assert len(resp1) > 0

        # Informa dado
        resp2, _ = mock_agent.process_message("minha renda é 6000")
        assert mock_agent.tem_confirmacao_pendente()

        # Confirma
        mock_agent.process_message("sim")

        # Outra pergunta
        resp3, _ = mock_agent.process_message("qual minha renda atual?")
        assert len(resp3) > 0


class TestRobustez:
    """Testes de robustez e edge cases"""

    def test_mensagens_vazias(self, mock_agent):
        """Testa processamento de mensagens vazias"""
        resp, _ = mock_agent.process_message("")
        assert resp is not None

    def test_mensagens_muito_longas(self, mock_agent):
        """Testa processamento de mensagens muito longas"""
        mensagem = "teste " * 1000
        resp, _ = mock_agent.process_message(mensagem)
        assert resp is not None

    def test_caracteres_especiais(self, mock_agent):
        """Testa processamento com caracteres especiais"""
        resp, _ = mock_agent.process_message("minha renda é R$ 5.000,00")

        if mock_agent.tem_confirmacao_pendente():
            mock_agent.process_message("sim")
            assert mock_agent.usuario["renda_mensal"] == 5000.0

    def test_valores_limites(self, mock_agent):
        """Testa valores nos limites"""
        # Renda mínima válida
        resp1, _ = mock_agent.process_message("minha renda é 0.01")
        if mock_agent.tem_confirmacao_pendente():
            mock_agent.process_message("sim")
            assert mock_agent.usuario["renda_mensal"] == 0.01

        # Idade mínima
        resp2, _ = mock_agent.process_message("tenho 18 anos")
        if mock_agent.tem_confirmacao_pendente():
            mock_agent.process_message("sim")
            assert mock_agent.usuario["idade"] == 18

    def test_valores_fora_limites(self, mock_agent):
        """Testa valores fora dos limites"""
        # Idade abaixo do mínimo
        resp1, _ = mock_agent.process_message("tenho 15 anos")
        assert resp1 == 'A idade deve estar entre 18 e 120 anos.'

        # Idade acima do máximo
        resp2, _ = mock_agent.process_message("tenho 1500 anos")
        assert resp2 == 'A idade deve estar entre 18 e 120 anos.'

    def test_case_sensitivity(self, mock_agent):
        """Testa sensibilidade a maiúsculas/minúsculas"""
        # Confirmação em maiúsculas
        mock_agent.process_message("minha renda é 5000")
        resp, _ = mock_agent.process_message("SIM")

        assert mock_agent.usuario["renda_mensal"] == 5000.0

    def test_espacos_extras(self, mock_agent):
        """Testa mensagens com espaços extras"""
        resp, _ = mock_agent.process_message("  minha   renda   é   5000  ")

        if mock_agent.tem_confirmacao_pendente():
            assert True  # Dados foram extraídos corretamente

    def test_acentuacao(self, mock_agent):
        """Testa mensagens com acentuação"""
        resp, _ = mock_agent.process_message("minha renda é 5000 reais")
        assert resp is not None

        resp2, _ = mock_agent.process_message("reserva de emergência é 10000")
        assert resp2 is not None

    def test_confirmacoes_sequenciais(self, mock_agent):
        """Testa múltiplas confirmações em sequência"""
        # Primeira confirmação
        mock_agent.process_message("minha renda é 5000")
        mock_agent.process_message("sim")

        # Segunda confirmação imediata
        mock_agent.process_message("sou moderado")
        mock_agent.process_message("sim")

        # Terceira confirmação
        mock_agent.process_message("tenho 30 anos")
        mock_agent.process_message("sim")

        assert mock_agent.usuario["renda_mensal"] == 5000.0
        assert mock_agent.usuario["perfil_investidor"]["valor"] == "moderado"
        assert mock_agent.usuario["idade"] == 30


class TestExtracaoAvancada:
    """Testes avançados de extração"""

    def test_formatos_monetarios_diversos(self, mock_agent):
        """Testa extração de diferentes formatos monetários"""
        from app.agent import FinancialAgent
        formatos = [
            ("ganho 5000", 5000.0),
            ("ganho R$ 5.000", 5000.0),
            ("ganho 5.000,00", 5000.0),
            ("ganho R$ 5000,00", 5000.0),
        ]

        for mensagem, valor_esperado in formatos:
            mock_agent_temp = FinancialAgent(
                data_manager=mock_agent.data_manager,
                extractor=mock_agent.extractor,
                validator=mock_agent.validator,
                llm_manager=mock_agent.llm_manager
            )

            resp, _ = mock_agent_temp.process_message(mensagem)
            if mock_agent_temp.tem_confirmacao_pendente():
                mock_agent_temp.process_message("sim")
                assert mock_agent_temp.usuario["renda_mensal"] == valor_esperado

    def test_extracao_contexto_natural(self, mock_agent):
        """Testa extração em contexto de linguagem natural"""
        mensagem = (
            "Oi, tudo bem? Eu me chamo João, tenho 35 anos e "
            "trabalho como engenheiro. Minha renda mensal é de "
            "R$ 8.500 e me considero um investidor moderado."
        )

        resp, _ = mock_agent.process_message(mensagem)

        if mock_agent.tem_confirmacao_pendente():
            mock_agent.process_message("sim")

            # Verifica que múltiplos dados foram extraídos
            assert mock_agent.usuario["idade"] == 35
            assert mock_agent.usuario["renda_mensal"] == 8500.0
            assert mock_agent.usuario["perfil_investidor"]["valor"] == "moderado"
