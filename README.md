# 🚀 Projeto: Agente de IA para Suporte Técnico (ALESC)

Este documento detalha a arquitetura, as tecnologias e a metodologia de **MLOps** aplicadas no desenvolvimento do Agente de Suporte Baseado em IA, projetado para otimizar o atendimento técnico da Assembleia Legislativa de Santa Catarina.

## 1. Escopo e Objetivo
Transformar uma base bruta de **50.000+ tickets do OTRS** em uma interface de linguagem natural capaz de fornecer diagnósticos precisos, soluções históricas e orientações de governança (SEI, Hardware, Redes) para o corpo técnico da ALESC, garantindo 100% de privacidade institucional.

## 2. Stack Tecnológica Atualizada

### Core e Interface
* **Linguagem:** Python 3.10+ (Ambiente Dockerizado).
* **Interface Web:** Streamlit (UI otimizada para produtividade).
* **Infraestrutura:** Docker & Docker Swarm (Orquestração de containers).

### Inteligência Artificial e RAG
* **LLM:** Google Gemini 3 Flash (Alta performance e baixa latência via REST).
* **Embeddings:** `paraphrase-multilingual-MiniLM-L12-v2` (SBERT).
* **Busca Vetorial:** FAISS (Facebook AI Similarity Search) com busca por proximidade de cosseno.

### Persistência e Auditoria (On-Premise)
* **Banco de Dados:** MySQL/MariaDB (Origem dos dados OTRS).
* **Logs de Auditoria:** JSON Local (Persistência em volume para conformidade com a LGPD, eliminando dependência de nuvem externa para logs).

---

## 🏗️ 3. Arquitetura do Sistema (MLOps Incremental)

O sistema utiliza a arquitetura **Retrieval-Augmented Generation (RAG)** com um pipeline de dados vivo:

1. **Ingestão Incremental:** O script de manutenção identifica apenas os novos chamados no OTRS e os adiciona ao índice existente, economizando recursos e tokens.
2. **Recuperação (Retrieval):** Localiza instantaneamente os precedentes técnicos mais relevantes no volume de dados.
3. **Geração (Generation):** A IA processa o contexto recuperado sob temperatura **0.1**, garantindo respostas técnicas fiéis ao histórico da ALESC.

---

## 📂 4. Estrutura de Diretórios (Padrão de Produção)

```text
/PROJETO_IA_ALESC
├── app.py                # Interface Streamlit
├── agente_motor.py       # Lógica da IA e Gravação de Logs
├── logica_busca.py       # Motor de busca semântica FAISS
├── database.py           # Driver de conexão MySQL
├── /data                 # VOLUME PERSISTENTE (HD Externo do Container)
│   ├── otrs_conhecimento.index
│   ├── otrs_mapping.csv
│   └── /logs             # Auditoria local (atendimentos.json)
├── /scripts              # Manutenção e Automação
│   └── indexador_otrs.py # Pipeline de atualização incremental
├── /assets               # Identidade visual (CSS)
├── Dockerfile            # Receita da imagem oficial
└── DEPLOY.md             # Manual técnico de implantação e Swarm