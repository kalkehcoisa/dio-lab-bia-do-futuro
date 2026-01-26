# ✅ Checklist — Desafio BIA do Futuro (DIO)

Checklist consolidada e refinada, mantendo o escopo original do desafio e organizada para facilitar validação técnica e avaliação.

---

## 📌 Comportamento do Agente
- [x] Atua de forma **proativa**, não apenas reativa
- [x] Sugere próximos passos ou reflexões relevantes ao contexto
- [x] Personaliza respostas com base nas informações fornecidas
- [x] Atua de forma consultiva (cocriação, não respostas prontas)
- [x] Mantém coerência de comportamento ao longo da conversa

---

## 💬 Interação e Linguagem Natural
- [x] Compreensão de linguagem natural (NLP)
- [x] Respostas claras, coerentes e contextualizadas
- [x] Manutenção de contexto durante a sessão
- [x] Linguagem acessível, sem jargões desnecessários
- [x] Capacidade de pedir esclarecimentos quando necessário

---

## 🧠 IA Generativa
- [x] Uso explícito de modelo de linguagem (LLM) — Groq API (Llama 3.3 70B)
- [x] Prompt base bem definido — `SYSTEM_PROMPT` em `src/app/agent.py`
- [x] Prompt com restrições claras de escopo
- [x] Separação entre geração de texto e regras de negócio
- [x] Tratamento explícito para perguntas fora do domínio

---

## 📊 Funcionalidades Principais
- [x] FAQs inteligentes (respostas dinâmicas e contextualizadas)
- [x] Simulações financeiras simples — LLM faz cálculos diretamente (prompt em `agent.py`)
- [x] Cálculos executados pelo LLM — parcelamento, juros compostos, reserva, etc.
- [x] Explicação clara dos resultados (prompt instrui a explicar metodologia)
- [x] Explicação de produtos financeiros comuns
- [x] Nenhuma recomendação financeira definitiva — bloqueio de termos em `config.py`

---

## 🧠 Contexto e Personalização
- [x] Persistência de contexto ao longo da conversa — `_squash_history()` em `agent.py`
- [x] Uso apenas de dados fornecidos pelo usuário — `_extract_facts()` usa só dados confirmados
- [x] Não assumir valores ou informações ausentes — prompt instrui a usar `null`
- [x] Solicitação explícita de dados obrigatórios
- [x] Contexto utilizado para ajustar respostas e exemplos — fatos injetados no prompt

---

## 🔐 Segurança e Anti-Alucinação
- [x] Escopo do agente claramente delimitado — `TERMOS_PROIBIDOS` em `config.py`
- [x] Estratégias documentadas de mitigação de alucinação — `01-documentacao-agente.md`
- [x] LLM não gera valores numéricos críticos — extrai do usuário, valida em `validation.py`
- [x] Respostas explicam como foram obtidas — prompt instrui a descrever metodologia
- [x] Declaração explícita de incerteza quando aplicável
- [x] Recusa segura de perguntas fora do escopo

---

## 🏗 Arquitetura da Solução
- [x] Arquitetura geral documentada — `01-documentacao-agente.md`
- [x] Diagrama da solução (Mermaid) — `01-documentacao-agente.md`
- [x] Componentes bem definidos — tabela em `01-documentacao-agente.md`
- [x] Separação clara entre interface, IA e lógica — `main.py`, `llm.py`, `agent.py`, `data.py`
- [x] Fluxo de dados e decisão descrito

---

## 🛠 Implementação
- [x] Código-fonte organizado e legível — `src/app/`
- [x] Estrutura de pastas clara — documentada no `README.md`
- [x] Dependências documentadas — `src/app/requirements.txt`
- [x] Instruções de execução do projeto — `README.md`
- [x] Interface simples para interação (chat) — Gradio em `main.py`
- [x] Projeto fácil de executar localmente — `python main.py`

---

## 📄 Documentação e Entrega
- [x] README.md completo
- [x] Caso de uso bem definido (problema, solução, público-alvo) — `01-documentacao-agente.md`
- [x] Persona do agente documentada — BIA em `01-documentacao-agente.md`
- [x] Tom de voz e exemplos de linguagem — `01-documentacao-agente.md`
- [x] Arquitetura descrita — diagrama Mermaid em `01-documentacao-agente.md`
- [x] Segurança e limitações documentadas — `01-documentacao-agente.md`
- [x] Repositório público no GitHub — [Repositório](https://github.com/kalkehcoisa/dio-lab-bia-do-futuro)

---

## 🧪 Demonstração
- [x] Exemplos reais de interação — `03-prompts.md`
- [x] Demonstração de uso de contexto — interface Gradio com botão "Mostrar dados"
- [x] Demonstração de simulação financeira — LLM calcula e explica diretamente
- [x] Evidência de funcionamento — `docs/06-evidencias.md`
- [x] Testes funcionais realizados — `tests/test_functional.py`
