# Avaliação e Métricas

## Objetivo
Definir indicadores, processos e procedimentos mensuráveis para avaliar qualidade, segurança, custo e desempenho do agente, com ligações claras ao código e aos testes do repositório.

## Fontes no projeto
- Agente: src/app/agent.py  
- Wrapper LLM (instrumentação): src/app/llm.py  
- Pré-processamento e anonimização: src/app/data.py  
- Testes e fixtures: tests/ — veja tests/test_llm.py e tests/test_validation.py

---

## Métricas principais (definições e como medir)
- Assertividade  
  - O que mede: % de respostas corretas vs. respostas esperadas em testes estruturados.  
  - Como medir: casos Q→A em `tests/` (contract tests) e cálculo de pass rate.

- Segurança (proteção de dados)  
  - O que mede: detecção de vazamento de dados sensíveis e recusa apropriada a solicitações proibidas.  
  - Como medir: testes negativos que solicitam dados sensíveis (ex.: CPF) e validação de respostas padrão.

- Coerência / Conformidade ao perfil  
  - O que mede: % de recomendações compatíveis com o perfil do usuário.  
  - Como medir: validações cruzadas entre fixtures de perfil e recomendações geradas.

- Latência  
  - O que mede: tempo médio por requisição (ms).  
  - Como medir: instrumentar chamadas em src/app/llm.py e registrar histogramas.

- Consumo de tokens / Custo  
  - O que mede: tokens request+response por chamada e custo estimado por provedor.  
  - Como medir: somar tokens por chamada no wrapper LLM e multiplicar pelo preço por 1k tokens.

- Estabilidade / Erros  
  - O que mede: taxa de exceções, timeouts e falhas por 1k requisições.  
  - Como medir: contagem de erros via logs estruturados.

- Cobertura de testes  
  - O que mede: porcentagem de cobertura para o código crítico.  
  - Como medir: `pytest --cov=src --cov-report=xml`

---

## Instrumentação prática (passos)
1. No wrapper LLM (src/app/llm.py), registrar por requisição:
   - `request_id`, `timestamp`, `duration_ms`, `tokens_request`, `tokens_response`, `status`, `error` (se houver).
2. Persistir logs/metrics em JSON/CSV ou enviar a um sistema de métricas (Prometheus).  
3. Adicionar testes automatizados para:
   - contratos de prompt (prompt montado → formato esperado),
   - vazamento de dados (respostas a solicitações sensíveis),
   - transformações de dados em src/app/data.py.
4. CI: rodar comandos
```bash
pytest --maxfail=1 --disable-warnings -q
pytest --cov=src --cov-report=xml
```
5. Rodar relatórios de custo: somar tokens diários × preço por 1k tokens.

---

## Testes recomendados
- Unit: validar transformações e normalizações em src/app/data.py.  
- Contract: fixtures que verificam o prompt composto e campos obrigatórios.  
- Integration (LLM mockado): validar fluxo do agente em tests/test_llm.py.  
- Functional / End-to-end: cenários reais cobrindo perguntas frequentes e edge-cases.  
- Avaliação humana (HITL): 3–5 avaliadores, N cenários, notas 1–5 para Assertividade / Clareza / Segurança.

---

## Tolerâncias operacionais (sugestões)
- Latência alvo (local): < 1500 ms  
- Assertividade alvo: ≥ 90% em contract tests automatizados  
- Segurança: 100% em testes de vazamento de dados (nenhum dado sensível retornado na íntegra)

---

## Registro e auditoria
- Guardar hashes dos prompts (sem dados sensíveis), versão do system prompt e versão do modelo usado.  
- Armazenar amostras truncadas/hashed das respostas para auditoria.  
- Gerar relatórios periódicos (diário/semana) com métricas agregadas: latência, erros, tokens e custo.

---

## Recomendações de evolução
- Automatizar coleta de tokens/custos no wrapper LLM.  
- Avaliar implementação de retriever + vetor DB para reduzir tokens e aumentar precisão.  
- Construir dashboard (Grafana ou CSV+notebook) com Latência, Erros, Tokens e Nota média humana.  
- Registrar experimentos (prompt/system prompt/temperatura) para reprodutibilidade.

---

## Próximos passos sugeridos
1. Instrumentar logs no wrapper LLM (src/app/llm.py).  
2. Adicionar contract tests e testes de vazamento em `tests/`.  
3. Configurar coleta automática de tokens e gerar relatório semanal de custo.
