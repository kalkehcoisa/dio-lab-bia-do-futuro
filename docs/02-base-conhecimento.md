# Base de Conhecimento

## Dados Utilizados

Os dados do projeto ficam em `src/data/` (fixtures/exemplos) e `src/app/data/` (dados de runtime). Arquivos usados no projeto:

| Arquivo | Local | Formato | Utilização no Agente |
|---------|-------|---------|---------------------|
| usuario.json | [src/app/data/usuario.json](../src/app/data/usuario.json) | JSON | Perfil do usuário (persistido em runtime) |
| interações | [src/app/data/interacoes/](../src/app/data/interacoes/) | JSON | Histórico de conversas salvas automaticamente |
| usuario.json (exemplo) | [src/data/usuario.json](../src/data/usuario.json) | JSON | Exemplo de perfil de usuário |
| transacoes.csv | [src/data/transacoes.csv](../src/data/transacoes.csv) | CSV | Exemplo de transações (fixture) |
| historico_financeiro.json | [src/data/historico_financeiro.json](../src/data/historico_financeiro.json) | JSON | Exemplo de histórico financeiro (fixture) |

Observação: o carregamento e a normalização centralizados estão implementados em [src/app/data.py](../src/app/data.py), que é chamado pelo agente em [src/app/agent.py](../src/app/agent.py).

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

Exemplo do bloco de contexto que o agente monta antes de enviar ao LLM (baseado no arquivo `src/data/usuario.json`):

```
INFORMAÇÕES DISPONÍVEIS DO USUÁRIO:
- Nome: João Silva
- Idade: 32 anos
- Profissão: Analista de Sistemas
- Renda mensal: R$ 5.000,00
- Patrimônio total: R$ 15.000,00
- Reserva de emergência: R$ 10.000,00
- Perfil de investidor: moderado
- Objetivo principal: Construir reserva de emergência
- Meta: Completar reserva de emergência - R$ 15.000,00 até 2026-06
- Meta: Entrada do apartamento - R$ 50.000,00 até 2027-12
```

Prompt composto (estrutura):
- **System prompt**: regras da BIA, formato de resposta JSON, restrições
- **System (contexto)**: fatos extraídos do perfil do usuário
- **Histórico**: mensagens anteriores da conversa (compactadas se necessário)
- **User**: mensagem atual do usuário

---

## Boas práticas e próximos passos

- Testes: atualize/adicione fixtures em `tests/` quando alterar o formato dos dados.
- Evolução: considerar vetorizar histórico e usar um retriever para consultas escaláveis.
- Operação: documentar scripts de atualização de dataset e sanitização na pasta `data/`.
