# 🤖 BIA — Assessora Financeira Pessoal com IA

## 📌 Visão Geral do Projeto

Este projeto apresenta a **BIA (Assessora Financeira Pessoal Conversacional)**, uma experiência digital guiada por **IA generativa**, focada em **educação financeira**, **organização de perfil financeiro** e **boas práticas de relacionamento com o usuário**.

A solução foi concebida para demonstrar a aplicação prática de conceitos de **inteligência artificial**, **Python**, **processamento de linguagem natural**, **modelagem de dados simples** e **experiência do usuário (UX)**, conforme proposto no desafio DIO.

O assistente interage em linguagem natural, mantém contexto durante a conversa, extrai e persiste dados do perfil do usuário, e oferece respostas claras, seguras e personalizadas, sempre com caráter educativo.

---

## 🎯 Objetivo

Criar um agente conversacional que atue como uma **assessora financeira pessoal**, capaz de:

* Compreender perguntas em linguagem natural
* Manter e atualizar um perfil financeiro do usuário ao longo da conversa
* Extrair automaticamente dados mencionados (renda, metas, patrimônio, etc.)
* Explicar conceitos e produtos financeiros de forma acessível
* Aplicar boas práticas de UX e comunicação responsável

A proposta **não é fornecer aconselhamento financeiro definitivo**, mas sim ajudar o usuário a entender cenários, conceitos e organizar suas informações financeiras.

---

## 🧠 Funcionalidades Principais

### 💬 Conversa em Linguagem Natural

O usuário pode interagir livremente com a assistente, fazendo perguntas como:

* "Consigo parcelar uma compra de R$ 3.000?"
* "Vale mais pagar à vista ou parcelar?"
* "Como funcionam os juros do cartão de crédito?"
* "Quais investimentos existem para quem ganha um salário mínimo?"

A IA interpreta a intenção antes de responder, oferecendo explicações contextualizadas.

---

### 👤 Perfil Financeiro Persistente

Durante a conversa, a BIA extrai e armazena automaticamente informações como:

* Nome, idade, profissão
* Renda mensal
* Perfil de investidor (conservador, moderado, arrojado)
* Patrimônio total e reserva de emergência
* Metas financeiras com valores e prazos

Os dados são persistidos em JSON e utilizados para personalizar as respostas.

---

### 📚 Educação Financeira

A assistente explica conceitos e produtos financeiros comuns, como:

* Cartão de crédito e juros
* Empréstimo pessoal
* Reserva de emergência
* Perfis de investidor

As respostas priorizam clareza, linguagem simples e exemplos práticos.

---

### 🔐 Boas Práticas de UX e Segurança

* Linguagem acessível e não técnica
* Avisos claros de que se trata de orientação educativa
* Nenhuma solicitação de dados sensíveis (CPF, senhas)
* Nenhuma recomendação financeira definitiva
* Bloqueio de termos proibidos relacionados a aconselhamento de investimentos

---

## 🚫 Fora do Escopo

Para manter o foco e a segurança da solução, não fazem parte deste projeto:

* Integração com APIs bancárias reais
* Investimentos ou recomendação de ativos específicos
* Autenticação de usuários
* Armazenamento de dados sensíveis (CPF, senhas, etc.)

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python 3.x** | Linguagem principal |
| **Gradio** | Interface conversacional web |
| **Groq API** | Provedor de LLM (Llama 3.3 70B) |
| **JSON/CSV** | Persistência de dados do usuário |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- Conta na [Groq](https://console.groq.com/) para obter uma API key

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd dio-lab-bia-do-futuro

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r src/app/requirements.txt

# Configure a API key
cd src/app
echo "GROQ_API_KEY=sua-chave-aqui" > .env
```

### Execução

```bash
cd src/app
python main.py
```

Acesse: http://localhost:7860

---

## ✅ Resultado Esperado

Ao utilizar a aplicação, o usuário consegue:

* Conversar naturalmente com a BIA
* Ter seu perfil financeiro extraído e persistido automaticamente
* Receber explicações claras e contextualizadas
* Visualizar seus dados coletados na interface
* Perceber a integração prática entre IA, Python, dados e UX

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [01-documentacao-agente.md](./docs/01-documentacao-agente.md) | Caso de uso, persona e arquitetura |
| [02-base-conhecimento.md](./docs/02-base-conhecimento.md) | Estratégia de dados e integração |
| [03-prompts.md](./docs/03-prompts.md) | Engenharia de prompts e exemplos |
| [04-metricas.md](./docs/04-metricas.md) | Avaliação e métricas |
| [05-pitch.md](./docs/05-pitch.md) | Roteiro do pitch |
| [06-evidencias.md](./docs/06-evidencias.md) | Evidências de funcionamento |
| [checklist.md](./docs/checklist.md) | Checklist de validação |

---

## 📁 Estrutura do Repositório

```
📁 dio-lab-bia-do-futuro/
│
├── 📄 README.md                      # Este arquivo
├── 📄 requirements-dev.txt           # Dependências de desenvolvimento
├── 📄 pytest.ini                     # Configuração de testes
│
├── 📁 docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados
│   ├── 03-prompts.md                 # Engenharia de prompts
│   ├── 04-metricas.md                # Avaliação e métricas
│   ├── 05-pitch.md                   # Roteiro do pitch
│   └── checklist.md                  # Checklist de validação
│
├── 📁 src/                           # Código-fonte
│   ├── 📁 app/                       # Aplicação principal
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point (Gradio)
│   │   ├── agent.py                  # Lógica do agente financeiro
│   │   ├── llm.py                    # Integração com Groq/LLM
│   │   ├── data.py                   # Gerenciamento de dados
│   │   ├── validation.py             # Validação de dados
│   │   ├── config.py                 # Configurações
│   │   ├── exceptions.py             # Exceções customizadas
│   │   ├── requirements.txt          # Dependências da aplicação
│   │   └── 📁 data/                  # Dados persistidos (runtime)
│   │       ├── usuario.json          # Perfil do usuário
│   │       └── 📁 interacoes/        # Histórico de conversas
│   │
│   └── 📁 data/                      # Dados de exemplo/fixtures
│       ├── usuario.json              # Exemplo de perfil
│       ├── transacoes.csv            # Exemplo de transações
│       ├── historico_financeiro.json # Exemplo de histórico
│       └── 📁 interacoes/            # Exemplos de interações
│
├── 📁 tests/                         # Testes automatizados
│   ├── conftest.py                   # Fixtures do pytest
│   ├── test_agent.py                 # Testes do agente
│   ├── test_data.py                  # Testes de dados
│   ├── test_llm.py                   # Testes do LLM
│   ├── test_validation.py            # Testes de validação
│   └── test_functional.py            # Testes funcionais
│
└── 📁 assets/                        # Imagens e diagramas
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html
```

---

## 📝 Licença

Este projeto foi desenvolvido para o desafio DIO — BIA do Futuro.
