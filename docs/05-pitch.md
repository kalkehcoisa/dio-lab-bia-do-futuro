# Pitch (3 minutos)

> Use este roteiro para apresentar a solução em até 3 minutos: problema, solução, demonstração curta, diferencial e call-to-action.

## Roteiro sugerido (script enxuto)

### 1. O Problema (30s)
- Usuários não têm visibilidade clara de hábitos de gastos nem recomendações práticas e personalizadas.
- Solução atual: dashboards genéricos ou consultoria cara e demorada.

### 2. A Solução (1min)
- Um agente conversacional que entende o perfil financeiro e as transações do usuário e entrega recomendações práticas e acionáveis em linguagem natural.
- Funcionalidades principais:
  - Resumo de saúde financeira (saldo, reserva, dívidas).
  - Sugestões de alocação simples (liquidez x rendimento).
  - Perguntas de esclarecimento automáticas quando faltam dados.
- Implementação: fluxo do agente em src/app/agent.py, LLM wrapper em src/app/llm.py e pré-processamento em src/app/data.py.

### 3. Demonstração (1min)
- Mostrar rapidamente (ao vivo ou vídeo):
  1. Iniciar o serviço local (ex.: script de execução ou `src/app/main.py`).
  2. Carregar dados de exemplo: data/usuario.json e data/transacoes.csv.
  3. Interação real: usuário pergunta "Como posso aumentar minha reserva de emergência com R$ 500 por mês?" — agente responde com resumo + plano de ação (ex.: dividir entre liquidez e CDB, passos práticos).
- Script curto para a demo (fala):
  - "Vou usar o perfil do usuário João (dados de exemplo) e pedir um plano de reserva com R$ 500/mês. O agente considera histórico de transações e propõe uma alocação prática e verificável."

### 4. Diferencial e Impacto (30s)
- Diferenciais técnicos:
  - Contextualização com dados reais do usuário (pré-processados e mascarados).
  - Regras de segurança para evitar vazamento de dados sensíveis e prompt-engineering robusto ([src/app/data.py], [src/app/llm.py]).
  - Testes automatizados cobrindo contratos de prompt e vazamentos (pasta `tests/`).
- Impacto:
  - Acesso rápido a recomendações pessoais, menor custo do que consultoria, aumento da literacia financeira do usuário.

---

## Métricas a mostrar no pitch (1–2 slides opcionais)
- Acurácia / assertividade em testes de contrato (ex.: % de respostas corretas).  
- Latência média por resposta (ms).  
- Redução estimada de custo operacional por atendimento (ex.: atendimentos humanos evitados).  
- Número de usuários simulados testados (HITL) e nota média.

---

## Demonstração técnica (detalhes rápidos)
- Pontos que podem aparecer em slides ou código:
  - Onde o prompt é montado: src/app/agent.py.  
  - Wrapping do provedor LLM: src/app/llm.py.  
  - Dados de entrada (exemplos): data/usuario.json, data/transacoes.csv.

---

## Checklist do Pitch (marcar antes de apresentar)
- [ ] Duração ≤ 3 minutos  
- [ ] Problema claramente definido  
- [ ] Solução demonstrada (ao vivo ou vídeo)  
- [ ] Pontos técnicos: arquitetura mínima, segurança e testes mencionados  
- [ ] Resultado mensurável ou chamada à ação (ex.: convite para teste / integração)

---

## Slide / Demo sugeridos (ordem)
1. Problema (1 slide)  
2. Solução + captura rápida da arquitetura (1 slide) — mostrar src/app/agent.py e flow simplificado  
3. Demo (vídeo 30–60s) ou demonstração ao vivo  
4. Métricas e próximos passos (1 slide) — como medir sucesso e roadmap

---

## Call-to-action (fechamento)
- Convite para testar com dados reais (sandbox), integrar via API ou colaborar para evolução (retriever/vectordb, dashboards).
- Contato / link para repositório e instruções rápidas de execução (mencionar README do projeto).

---

## Link do Vídeo
- Cole aqui o link do seu pitch (YouTube, Loom, Google Drive, etc.)

[Link do vídeo]
