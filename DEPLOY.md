# 🚀 Guia de Implantação e MLOps - Agente IA ALESC

Este documento detalha os requisitos, a arquitetura de containers e a estratégia de **Atualização Contínua e Incremental** para o Agente de Suporte Técnico.

---

## 📋 1. Ficha Técnica de Infraestrutura

### Requisitos de Hardware (Sizing)
* **Memória RAM:** Mínimo 1GB | Recomendado 2GB (Reserva para busca vetorial em memória).
* **CPU:** 1 vCPU (Processamento de IA via API Google Gemini).
* **Disco:** ~500MB (Imagem Docker) + Espaço para o Volume de Dados (~1GB a 2GB).

### Variáveis de Ambiente (Secrets)
Configuradas via arquivo `.env` ou Docker Secrets:
* `GOOGLE_API_KEY`: Chave de autenticação da API Gemini.

---

## 🔄 2. Estratégia de Atualização Incremental (MLOps)

Para manter o Agente atualizado com o OTRS sem custos excessivos de API, utilizamos uma abordagem **Incremental**.

### Fluxo de Funcionamento:
1. **Identificação:** O script `scripts/indexador_otrs.py` verifica o último ID processado no arquivo `data/otrs_mapping.csv`.
2. **Vetorização Parcial:** Apenas os chamados novos (`ID > last_id`) são convertidos em embeddings.
3. **Merge (Hot Reload):** Os novos vetores são adicionados ao índice FAISS em tempo real. Como o container lê os arquivos via **Volume**, ele incorpora o novo conhecimento instantaneamente.

---

## 🐳 3. Arquitetura de Containers (Docker & Swarm)

### Estratégia de Volumes
Fundamental para persistência da base de conhecimento e dos logs de auditoria local.

**Configuração do `docker-compose.yml`:**
```yaml
services:
  agente-ti-alesc:
    image: agente-ti-alesc:latest
    ports:
      - "8501:8501"
    env_file: .env
    volumes:
      - /opt/alesc/agente_ia/data:/app/data  # Base de dados e Logs
    deploy:
      resources:
        limits:
          memory: 2G