# 📸 Evidências de Funcionamento

Este documento apresenta exemplos de interação com a BIA, demonstrando as principais funcionalidades do agente.

---

## 1. Mensagem de Boas-Vindas

Ao iniciar a aplicação, o usuário recebe uma mensagem de boas-vindas:

```
Olá!

Sou a BIA, sua assistente financeira pessoal. Estou aqui para ajudar você a:

- Organizar suas informações financeiras
- Acompanhar suas metas
- Entender melhor seu perfil financeiro
- Aprender sobre educação financeira

Alguns exemplos de perguntas:
- Consigo parcelar uma compra de R$ 3.000?
- Vale mais pagar à vista ou parcelar?
- Como funcionam os juros do cartão de crédito?
- Quais investimentos existem para quem ganha um salário mínimo?

Como posso ajudar você hoje?
```

---

## 2. Extração Automática de Dados

### Entrada do Usuário:
```
Meu nome é Maria, tenho 28 anos e trabalho como desenvolvedora. 
Minha renda mensal é R$ 8.000.
```

### Resposta da BIA:
```json
{
  "resposta": "Olá, Maria! Prazer em conhecê-la! 👋\n\nEntendi que você tem 28 anos, trabalha como desenvolvedora e tem uma renda mensal de R$ 8.000. Essas informações vão me ajudar a personalizar nossas conversas sobre finanças.\n\nComo posso ajudá-la hoje? Posso ajudar com:\n- Organização financeira\n- Simulações de parcelamento\n- Planejamento de reserva de emergência\n- Educação financeira em geral",
  "user_message": "Meu nome é Maria...",
  "dados_extraidos": {
    "renda_mensal": 8000.0,
    "perfil_investidor": null,
    "idade": 28,
    "profissao": "desenvolvedora",
    "patrimonio_total": null,
    "reserva_emergencia_atual": null,
    "metas": null
  }
}
```

### Perfil Atualizado (usuario.json):
```json
{
  "nome": null,
  "idade": 28,
  "profissao": "desenvolvedora",
  "renda_mensal": 8000.0,
  "perfil_investidor": {
    "valor": null,
    "confirmado": false
  },
  "objetivo_principal": {
    "descricao": null,
    "confirmado": false
  },
  "patrimonio_total": null,
  "reserva_emergencia_atual": null,
  "aceita_risco": false,
  "metas": [],
  "ultima_atualizacao": "2026-01-26 15:30:00"
}
```

---

## 3. Simulação de Parcelamento

### Entrada do Usuário:
```
Quanto fica uma compra de R$ 3.000 em 10x com juros de 2% ao mês?
```

### Resposta da BIA:
```
Vou calcular o parcelamento para você!

**Resultado:**
- Valor da parcela: R$ 333,98
- Total a pagar: R$ 3.339,80
- Juros total: R$ 339,80

**Cálculo (Tabela Price):**
Com juros de 2% ao mês em 10 parcelas, a parcela fixa é calculada 
considerando que você paga um pouco de juros e um pouco do principal 
a cada mês.

**Observação:** Esse valor pode variar dependendo da instituição 
financeira. Sempre confirme as condições antes de fechar a compra!
```

---

## 4. Comparação À Vista vs Parcelado

### Entrada do Usuário:
```
Vale mais pagar R$ 2.800 à vista ou R$ 3.000 em 10x sem juros?
```

### Resposta da BIA:
```
Vamos analisar as duas opções:

**À vista:** R$ 2.800
**Parcelado (10x):** R$ 3.000 (parcelas de R$ 300)

**Diferença:** R$ 200 (7,1% a mais no parcelado)

**Análise:**
À vista você economiza R$ 200. Mas se você investir os R$ 2.800 
a uma taxa de 1% ao mês durante 10 meses, teria aproximadamente 
R$ 3.094 ao final.

**Conclusão:** Se você tem o dinheiro e pode investir, pagar 
parcelado e deixar o dinheiro rendendo pode ser mais vantajoso. 
Mas se não for investir, pagar à vista e economizar os R$ 200 
é a melhor escolha.

Lembre-se: essa é uma análise educativa, não uma recomendação 
de investimento específico.
```

---

## 5. Planejamento de Reserva de Emergência

### Entrada do Usuário:
```
Quanto tempo levo para ter uma reserva de 6 meses ganhando R$ 5.000 
e conseguindo poupar R$ 500 por mês?
```

### Resposta da BIA:
```
Vamos calcular sua reserva de emergência!

**Meta:** R$ 30.000 (6 meses × R$ 5.000)
**Aporte mensal:** R$ 500

**Tempo estimado:** 60 meses (5 anos)

**Dica:** Se você conseguir aumentar o aporte para R$ 1.000/mês, 
atingiria a meta em 30 meses (2,5 anos).

A reserva de emergência deve ficar em investimentos de alta 
liquidez, como Tesouro Selic ou CDB com liquidez diária.
```

---

## 6. Persistência de Contexto

### Primeira mensagem:
```
Minha renda é R$ 6.000 e tenho R$ 10.000 guardados.
```

### Segunda mensagem:
```
Quero comprar um carro de R$ 50.000. Consigo?
```

### Resposta da BIA (usando contexto):
```
Com base nas informações que você me passou:
- Renda mensal: R$ 6.000
- Reserva atual: R$ 10.000

Para um carro de R$ 50.000, considerando uma entrada de 20% 
(R$ 10.000 - sua reserva atual), você financiaria R$ 40.000.

**Simulação de financiamento (48 meses, 1,5% a.m.):**
- Parcela aproximada: R$ 1.180
- Comprometimento da renda: 19,7%

**Atenção:** Usar toda sua reserva como entrada pode ser arriscado. 
O ideal é manter pelo menos 3-6 meses de despesas como emergência.

Você gostaria que eu simule outras opções de prazo ou entrada?
```

---

## 7. Bloqueio de Recomendações de Investimento

### Entrada do Usuário:
```
Em qual ação devo investir meu dinheiro?
```

### Resposta da BIA:
```
Não posso fazer recomendações de investimentos específicos, 
como indicar ações, fundos ou ativos.

Posso ajudá-la com:
- Explicar tipos de investimentos (renda fixa, variável, etc.)
- Simular cenários de poupança e juros compostos
- Organizar suas informações financeiras
- Entender seu perfil de investidor

Para recomendações específicas de investimento, sugiro consultar 
um assessor de investimentos certificado.

Posso ajudar com alguma dessas opções?
```

---

## 8. Interface Gradio

A interface web (http://localhost:7860) oferece:

1. **Chat interativo** - Conversa em tempo real com a BIA
2. **Botão "Mostrar dados"** - Visualiza o perfil extraído
3. **Histórico persistente** - Contexto mantido durante a sessão

### Como executar:
```bash
cd src/app
python main.py
# Acesse: http://localhost:7860
```

---

## 9. Estrutura de Dados Persistidos

### usuario.json (após interações):
```json
{
  "nome": "Maria",
  "idade": 28,
  "profissao": "desenvolvedora",
  "renda_mensal": 8000.0,
  "perfil_investidor": {
    "valor": "moderado",
    "confirmado": true
  },
  "objetivo_principal": {
    "descricao": "Comprar apartamento",
    "confirmado": true
  },
  "patrimonio_total": 25000.0,
  "reserva_emergencia_atual": 15000.0,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 80000.0,
      "prazo": "2028-12",
      "confirmado": true
    }
  ],
  "ultima_atualizacao": "2026-01-26 16:45:00"
}
```

### Histórico de interações (src/app/data/interacoes/):
```
2026-01-26_153000.json
2026-01-26_153245.json
2026-01-26_154500.json
```

---

## 10. Testes Automatizados

```bash
$ pytest tests/test_validation.py -v

tests/test_validation.py::TestDataValidator::test_validate_answer_vazia PASSED
tests/test_validation.py::TestDataValidator::test_validar_renda_valida PASSED
tests/test_validation.py::TestDataValidator::test_validar_renda_negativa PASSED
tests/test_validation.py::TestDataValidator::test_validar_perfil_conservador PASSED
tests/test_validation.py::TestDataValidator::test_validar_perfil_moderado PASSED
tests/test_validation.py::TestDataValidator::test_validar_perfil_arrojado PASSED
...
============================== 35 passed ==============================
```

---

## Resumo das Evidências

| Funcionalidade | Status | Evidência |
|----------------|--------|-----------|
| Boas-vindas personalizadas | ✅ | Seção 1 |
| Extração de dados do usuário | ✅ | Seção 2 |
| Simulação de parcelamento | ✅ | Seção 3 |
| Comparação à vista/parcelado | ✅ | Seção 4 |
| Reserva de emergência | ✅ | Seção 5 |
| Persistência de contexto | ✅ | Seção 6 |
| Bloqueio de recomendações | ✅ | Seção 7 |
| Interface Gradio | ✅ | Seção 8 |
| Persistência de dados | ✅ | Seção 9 |
| Testes automatizados | ✅ | Seção 10 |
