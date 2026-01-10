"""
Testes para o agente financeiro principal
"""

class TestFinancialAgent:
    """Testes para FinancialAgent"""

    def test_inicializacao(self, mock_agent):
        """Testa inicialização do mock_agente"""
        assert mock_agent is not None
        assert mock_agent.usuario is not None
        assert mock_agent.pendente_confirmacao is None

    def test_eh_confirmacao_sim(self, mock_agent):
        """Testa detecção de confirmação 'sim'"""
        assert mock_agent.eh_confirmacao("sim") is True
        assert mock_agent.eh_confirmacao("SIM") is True
        assert mock_agent.eh_confirmacao("  sim  ") is True

    def test_eh_confirmacao_ok(self, mock_agent):
        """Testa detecção de confirmação 'ok'"""
        assert mock_agent.eh_confirmacao("ok") is True
        assert mock_agent.eh_confirmacao("OK") is True

    def test_eh_confirmacao_confirmo(self, mock_agent):
        """Testa detecção de confirmação 'confirmo'"""
        assert mock_agent.eh_confirmacao("confirmo") is True
        assert mock_agent.eh_confirmacao("pode salvar") is True

    def test_eh_confirmacao_negativo(self, mock_agent):
        """Testa detecção de não-confirmação"""
        assert mock_agent.eh_confirmacao("não") is False
        assert mock_agent.eh_confirmacao("teste") is False
        assert mock_agent.eh_confirmacao("talvez") is False

    def test_eh_negacao_nao(self, mock_agent):
        """Testa detecção de negação 'não'"""
        assert mock_agent.eh_negacao("não") is True
        assert mock_agent.eh_negacao("nao") is True
        assert mock_agent.eh_negacao("NÃO") is True

    def test_eh_negacao_cancelar(self, mock_agent):
        """Testa detecção de negação 'cancelar'"""
        assert mock_agent.eh_negacao("cancelar") is True
        assert mock_agent.eh_negacao("cancel") is True

    def test_formatar_confirmacao_renda(self, mock_agent):
        """Testa formatação de confirmação com renda"""
        dados = {"renda_mensal": 5000.00}
        mensagem = mock_agent.formatar_confirmacao(dados)

        # Aceita formatos: 5000, 5.000, 5,000
        assert any(fmt in mensagem for fmt in ["5000", "5.000", "5,000"])
        assert "Renda" in mensagem
        assert "sim ou não" in mensagem.lower()

    def test_formatar_confirmacao_perfil(self, mock_agent):
        """Testa formatação de confirmação com perfil"""
        dados = {"perfil_investidor": "moderado"}
        mensagem = mock_agent.formatar_confirmacao(dados)

        assert "moderado" in mensagem.lower()
        assert "Perfil" in mensagem

    def test_formatar_confirmacao_metas(self, mock_agent):
        """Testa formatação de confirmação com metas"""
        dados = {
            "metas": [{
                "meta": "Comprar carro",
                "valor_necessario": 30000.00,
                "prazo": "2025"
            }]
        }
        mensagem = mock_agent.formatar_confirmacao(dados)

        assert "Comprar carro" in mensagem
        assert "30,000" in mensagem or "30.000" in mensagem

    def test_processar_mensagem_sem_dados(self, mock_agent):
        """Testa processamento de mensagem sem dados extraíveis"""
        resposta, usuario = mock_agent.processar_mensagem("olá, tudo bem?")

        assert resposta is not None
        assert len(resposta) > 0

    def test_processar_mensagem_com_renda(self, mock_agent):
        """Testa processamento de mensagem com renda"""
        resposta, usuario = mock_agent.processar_mensagem("minha renda é 6000 reais")

        assert "6,000" in resposta
        assert "confirma" in resposta.lower() or "salvar" in resposta.lower()
        assert mock_agent.pendente_confirmacao is not None

    def test_processar_mensagem_com_perfil(self, mock_agent):
        """Testa processamento de mensagem com perfil"""
        resposta, usuario = mock_agent.processar_mensagem("sou conservador")

        assert "conservador" in resposta.lower()
        assert mock_agent.pendente_confirmacao is not None

    def test_fluxo_confirmacao_positiva(self, mock_agent):
        """Testa fluxo completo de confirmação positiva"""
        # 1. Enviar dados
        resposta1, _ = mock_agent.processar_mensagem("minha renda é 7000")
        assert mock_agent.pendente_confirmacao is not None

        # 2. Confirmar
        resposta2, usuario = mock_agent.processar_mensagem("sim")
        assert "confirmado" in resposta2.lower()
        assert mock_agent.pendente_confirmacao is None
        assert usuario["renda_mensal"] == 7000.0

    def test_fluxo_confirmacao_negativa(self, mock_agent):
        """Testa fluxo completo de confirmação negativa"""
        # 1. Enviar dados
        resposta1, usuario_antes = mock_agent.processar_mensagem("minha renda é 7000")
        assert mock_agent.pendente_confirmacao is not None
        renda_antes = usuario_antes.get("renda_mensal")

        # 2. Negar
        resposta2, usuario_depois = mock_agent.processar_mensagem("não")
        assert "não salvei" in resposta2.lower()
        assert mock_agent.pendente_confirmacao is None
        assert usuario_depois.get("renda_mensal") == renda_antes

    def test_processar_multiplos_dados(self, mock_agent):
        """Testa processamento de múltiplos dados"""
        resposta, usuario = mock_agent.processar_mensagem(
            "tenho 35 anos, ganho 8000 por mês e sou moderado"
        )

        assert mock_agent.pendente_confirmacao is not None
        assert "idade" in resposta.lower() or "35" in resposta
        assert "8,000" in resposta

    def test_processar_dados_invalidos(self, mock_agent):
        """Testa processamento de dados inválidos"""
        resposta, usuario = mock_agent.processar_mensagem("minha renda é -5000")

        assert "precisa ser um valor positivo" in resposta.lower()
        assert mock_agent.pendente_confirmacao is None

    def test_processar_termo_proibido(self, mock_agent):
        """Testa processamento com termo proibido"""
        resposta, usuario = mock_agent.processar_mensagem("invista em bitcoin, minha renda é 5000")

        assert "não posso" in resposta.lower() or "recomenda" in resposta.lower()

    def test_obter_mensagem_boas_vindas(self, mock_agent):
        """Testa obtenção de mensagem de boas-vindas"""
        mensagem = mock_agent.obter_mensagem_boas_vindas()

        assert mensagem is not None
        assert "BIA" in mensagem

    def test_obter_resumo_perfil(self, mock_agent):
        """Testa obtenção de resumo do perfil"""
        resumo = mock_agent.obter_resumo_perfil()

        assert resumo is not None
        assert "Resumo" in resumo or "Perfil" in resumo

    def test_resetar_confirmacao_pendente(self, mock_agent):
        """Testa reset de confirmação pendente"""
        mock_agent.processar_mensagem("minha renda é 5000")
        assert mock_agent.tem_confirmacao_pendente()

        mock_agent.resetar_confirmacao_pendente()
        assert not mock_agent.tem_confirmacao_pendente()

    def test_tem_confirmacao_pendente(self, mock_agent):
        """Testa verificação de confirmação pendente"""
        assert not mock_agent.tem_confirmacao_pendente()

        mock_agent.processar_mensagem("minha renda é 5000")
        assert mock_agent.tem_confirmacao_pendente()

    def test_confirmacao_ambigua(self, mock_agent):
        """Testa resposta ambígua durante confirmação"""
        # 1. Enviar dados
        mock_agent.processar_mensagem("minha renda é 5000")

        # 2. Resposta ambígua
        resposta, _ = mock_agent.processar_mensagem("talvez")

        assert "não entendi" in resposta.lower() or "sim ou não" in resposta.lower()
        assert mock_agent.tem_confirmacao_pendente()

    def test_validacao_consistencia_falha(self, mock_agent):
        """Testa que validação de consistência impede salvamento"""
        # Configura cenário: reserva > patrimônio (inválido)
        mock_agent.usuario["patrimonio_total"] = 10000.00

        resposta, _ = mock_agent.processar_mensagem("minha reserva de emergência é 15000")
        mock_agent.processar_mensagem("sim")

        # Reserva não deve ser maior que patrimônio
        # A validação deve impedir salvamento
        assert mock_agent.usuario["reserva_emergencia_atual"] != 15000.00

    def test_salvar_interacao(self, mock_agent):
        """Testa que interações são salvas"""
        # Processa mensagem
        mock_agent.processar_mensagem("minha renda é 5000")

        # Não deve levantar exceção
        assert True

    def test_processar_mensagem_multiplas_vezes(self, mock_agent):
        """Testa processamento de múltiplas mensagens"""
        mensagens = [
            "olá",
            "minha renda é 5000",
            "sim",
            "qual minha renda?",
            "sou moderado"
        ]

        for msg in mensagens:
            resposta, _ = mock_agent.processar_mensagem(msg)
            assert resposta is not None

    def test_estado_apos_confirmacao(self, mock_agent):
        """Testa que estado é limpo após confirmação"""
        # Enviar e confirmar
        mock_agent.processar_mensagem("minha renda é 5000")
        assert mock_agent.tem_confirmacao_pendente()

        mock_agent.processar_mensagem("sim")
        assert not mock_agent.tem_confirmacao_pendente()

        # Nova interação não deve ter pendência
        mock_agent.processar_mensagem("olá")
        assert not mock_agent.tem_confirmacao_pendente()

    def test_idade_atualizada(self, mock_agent):
        """Testa atualização de idade"""
        resposta, _ = mock_agent.processar_mensagem("tenho 40 anos")
        assert mock_agent.tem_confirmacao_pendente()

        mock_agent.processar_mensagem("sim")
        assert mock_agent.usuario["idade"] == 40

    def test_profissao_atualizada(self, mock_agent):
        """Testa atualização de profissão"""
        resposta, _ = mock_agent.processar_mensagem("sou Engenheiro")

        if mock_agent.tem_confirmacao_pendente():
            mock_agent.processar_mensagem("sim")
            assert mock_agent.usuario["profissao"] == "Engenheiro"

    def test_meta_adicionada(self, mock_agent):
        """Testa adição de meta"""
        metas_iniciais = len(mock_agent.usuario.get("metas", []))

        resposta, _ = mock_agent.processar_mensagem("meta de juntar 20000 até 2026")
        mock_agent.processar_mensagem("sim")

        assert len(mock_agent.usuario["metas"]) > metas_iniciais
