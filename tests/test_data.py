def test_aplica_atualizacao_simples():
    from app.data import aplicar_atualizacoes

    usuario = {"renda_mensal": 3000}
    novos_dados = {"renda_mensal": 5000}

    atualizado = aplicar_atualizacoes(usuario, novos_dados)

    assert atualizado["renda_mensal"] == 5000
