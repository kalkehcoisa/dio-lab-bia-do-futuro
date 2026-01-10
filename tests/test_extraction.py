def test_detecta_renda_mensal():
    from app.extraction import detectar_novos_dados

    texto = "Minha renda mensal agora é 6500"
    dados = detectar_novos_dados(texto)

    assert dados == {"renda_mensal": 6500.0}


def test_detecta_patrimonio():
    from app.extraction import detectar_novos_dados

    texto = "Meu patrimônio é 20000"
    dados = detectar_novos_dados(texto)

    assert dados == {"patrimonio_total": 20000.0}


def test_texto_sem_dados():
    from app.extraction import detectar_novos_dados

    texto = "Olá, tudo bem?"
    dados = detectar_novos_dados(texto)

    assert dados == {}


def test_usuario_vazio():
    from app.validation import extrair_fatos_permitidos

    assert extrair_fatos_permitidos({}) == set()


def test_extrai_dados_basicos():
    from app.validation import extrair_fatos_permitidos

    usuario = {
        "nome": "João",
        "idade": 30,
        "profissao": "Analista",
        "renda_mensal": 5000,
        "patrimonio_total": 10000,
        "reserva_emergencia_atual": 8000
    }

    fatos = extrair_fatos_permitidos(usuario)

    assert "João" in fatos
    assert "30" in fatos
    assert "Analista" in fatos
    assert "5000" in fatos


def test_nao_extrai_nao_confirmado():
    from app.validation import extrair_fatos_permitidos

    usuario = {
        "perfil_investidor": {
            "valor": "moderado",
            "confirmado": False
        }
    }

    fatos = extrair_fatos_permitidos(usuario)

    assert "moderado" not in fatos


def test_extrai_confirmado():
    from app.validation import extrair_fatos_permitidos

    usuario = {
        "perfil_investidor": {
            "valor": "moderado",
            "confirmado": True
        }
    }

    fatos = extrair_fatos_permitidos(usuario)

    assert "moderado" in fatos
