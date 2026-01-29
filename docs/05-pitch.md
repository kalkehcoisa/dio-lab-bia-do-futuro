# Pitch (3 minutos)

> Use este roteiro para apresentar a solução em até 3 minutos: problema, solução, demonstração curta, diferencial e call-to-action.

## Roteiro sugerido (script enxuto)

### 1. O Problema (30s)
- Usuários não têm visibilidade clara de hábitos de gastos nem recomendações práticas e personalizadas.
- Solução atual: dashboards genéricos ou consultoria cara e demorada.

### 2. A Solução (1min)
- **BIA**: uma assistente financeira conversacional que extrai automaticamente o perfil do usuário e entrega orientações educativas em linguagem natural.
- Funcionalidades principais:
  - Extração automática de dados financeiros da conversa (renda, metas, patrimônio)
  - Persistência do perfil do usuário em JSON
  - Orientação educativa sem recomendação de investimentos específicos
  - Perguntas de esclarecimento automáticas quando faltam dados.
- Implementação: 
  - Agente: [src/app/agent.py](../src/app/agent.py)
  - LLM (Groq): [src/app/llm.py](../src/app/llm.py)
  - Dados: [src/app/data.py](../src/app/data.py)

### 3. Demonstração (1min)
- Mostrar rapidamente (ao vivo ou vídeo):
  1. Iniciar o serviço: `cd src/app && python main.py`
  2. Acessar http://localhost:7860
  3. Interação real: usuário informa dados ("Minha renda é R$ 5.000") e a BIA extrai automaticamente.
  4. Clicar em "Mostrar dados" para ver o perfil sendo atualizado em tempo real.
- Script curto para a demo (fala):
  - "Vou conversar com a BIA informando minha renda e metas. Vejam como ela extrai os dados automaticamente e personaliza as respostas com base no meu perfil."

### 4. Diferencial e Impacto (30s)
- Diferenciais técnicos:
  - **Extração automática de dados**: a BIA identifica e persiste informações financeiras da conversa
  - **Resposta estruturada**: LLM retorna JSON que separa resposta de dados extraídos
  - **Segurança**: bloqueio de termos proibidos (investimentos específicos), validação de dados
  - **Testes automatizados**: cobertura em [tests/](../tests/)
- Impacto:
  - Organização financeira acessível e gratuita
  - Aumento da literacia financeira do usuário
  - Demonstração prática de integração IA + Python + UX

---

## Métricas a mostrar no pitch (1–2 slides opcionais)
- Acurácia / assertividade em testes de contrato (ex.: % de respostas corretas).  
- Latência média por resposta (ms).  
- Redução estimada de custo operacional por atendimento (ex.: atendimentos humanos evitados).  
- Número de usuários simulados testados (HITL) e nota média.

---

## Demonstração técnica (detalhes rápidos)
- Pontos que podem aparecer em slides ou código:
  - Onde o prompt é montado: [src/app/agent.py](../src/app/agent.py)
  - Wrapping do provedor LLM: [src/app/llm.py](../src/app/llm.py) (Groq API)
  - Dados persistidos: [src/app/data/usuario.json](../src/app/data/usuario.json)
  - Interface: [src/app/main.py](../src/app/main.py) (Gradio)

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
[Vídeo no youtube](https://youtu.be/LJTW_4rYys8)