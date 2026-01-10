def test_valido_quando_dados_ok():
    from app.validation import validar_resposta

    dados = {"renda_mensal": 5000}
    valido, erro = validar_resposta(dados, "minha renda é 5000")

    assert valido is True
    assert erro is None


def test_bloqueia_termo_proibido():
    from app.validation import validar_resposta

    dados = {"renda_mensal": 4000}
    valido, erro = validar_resposta(dados, "recomendo investir em ações")

    assert valido is False
    assert erro is not None


def test_dados_vazios_invalidos():
    from app.validation import validar_resposta

    valido, erro = validar_resposta({}, "qualquer coisa")

    assert valido is False
    assert erro is not None
