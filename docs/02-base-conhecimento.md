# Base de Conhecimento

## Dados Utilizados

Os dados do projeto ficam em `src/data/` e são consumidos pelo agente em `src/app/`. Arquivos usados no projeto:

| Arquivo | Local | Formato | Utilização no Agente |
|---------|-------|---------|---------------------|
| historico_financeiro.json | [src/data/historico_financeiro.json](src/data/historico_financeiro.json) | JSON | Perfil financeiro histórico do usuário (resumo, empréstimos, investimentos) |
| transacoes.csv | [src/data/transacoes.csv](src/data/transacoes.csv) | CSV | Lista de transações usadas para identificar padrões de gasto recentes |
| usuario.json | [src/data/usuario.json](src/data/usuario.json) | JSON | Dados cadastrais e preferências do usuário |
| interações (mock) | [src/app/data.py](src/app/data.py) / [src/data/interacoes/](src/data/interacoes/) | JSON/CSV | Histórico de conversas / interações usadas para contextualizar diálogo |

Observação: o carregamento e a normalização centralizados estão implementados em [src/app/data.py](src/app/data.py), que é chamado pelo agente em [src/app/agent.py](src/app/agent.py).

---

## Adaptações nos Dados

- Estado atual: os arquivos no repositório são mocks/fixtures destinados a testes e demonstração; não alterei os dados originais.
- Recomendações de adaptação:
  - Anonimizar campos sensíveis (CPF, e-mail) para uso em demos.
  - Normalizar datas para ISO (`YYYY-MM-DD`) e valores monetários para formato numérico.
  - Agregar transações recentes (últimos 3 meses) para reduzir o contexto do prompt.
  - Adicionar um campo `source` nas entradas quando combinar múltiplas bases (ex.: `historico_financeiro`, `transacoes`, `usuario`).

Exemplo de transformação simples (pseudo):
- Ler `transacoes.csv` → converter `valor` para float → ordenar por data → manter últimas N linhas.

---

## Estratégia de Integração

- Onde o carregamento acontece:
  - `src/app/data.py` contém funções utilitárias para leitura e transformação de `JSON`/`CSV`.
  - `src/app/agent.py` compõe o contexto usando as funções de `data.py` antes de acionar o LLM via `src/app/llm.py`.

- Escopo e frequência:
  - Dados estáticos (perfil do usuário) são carregados no início da sessão e mantidos em cache por sessão.
  - Dados dinâmicos (últimas transações, interações recentes) são consultados a cada requisição para garantir atualidade.

- Como os dados entram no prompt:
  - Perfil resumido e recomendações-chave são injetados no system prompt como contexto de domínio.
  - Trechos relevantes (últimas 5-10 transações, últimos 3 intercâmbios) são concatenados ao user prompt como memória de curto prazo.
  - Para bases maiores, usar um passo de recuperação (retrieval) e inserir apenas trechos relevantes no prompt (padrão não implementado, sugerido como evolução).

- Segurança e limites:
  - Aplicar truncamento e sumarização quando o contexto exceder o limite de tokens do LLM.
  - Remover ou mascarar dados sensíveis antes de enviar ao LLM.

---

## Exemplo de Contexto Montado

Exemplo do bloco de contexto que o agente monta antes de enviar ao LLM:

Dados do Cliente:
- Nome: João Silva
- Perfil de investimento: Moderado
- Renda mensal: R$ 8.000
- Objetivo: Reserva de emergência (12 meses)

Resumo financeiro:
- Saldo atual (conta corrente): R$ 3.200
- Investimentos liquidez alta: R$ 7.500
- Dívidas: R$ 0

Últimas transações (ultimas 5):
- 2025-11-01: Supermercado — R$ 450
- 2025-11-03: Streaming — R$ 55
- 2025-11-05: Farmácia — R$ 78
- 2025-11-07: Restaurante — R$ 120
- 2025-11-10: Conta de luz — R$ 210

Prompt composto (resumo):
- System: contexto do domínio + políticas (limitar recomendações a produtos existentes).
- User: pergunta do usuário + bloco "Dados do Cliente" + "Últimas transações".

---

## Boas práticas e próximos passos

- Testes: atualize/adicione fixtures em `tests/` quando alterar o formato dos dados.
- Evolução: considerar vetorizar histórico e usar um retriever para consultas escaláveis.
- Operação: documentar scripts de atualização de dataset e sanitização na pasta `data/`.
