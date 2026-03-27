# 🛡️ Guia de Implantação - Agente de IA (ALESC)

**Versão:** 6.0 (Final - Full Spec)  
**Ambiente:** Homologação ALESC  
**Responsável Técnico:** Edson Bez  

---

## 1. Procedimento de Aquisição do Código (Clonagem e Setup)

Para iniciar a implantação no servidor de homologação da ALESC, siga a sequência abaixo:

```bash
# 1. Navegar para o diretório de aplicações opcionais
cd /opt

# 2. Criar estrutura de diretórios da ALESC
sudo mkdir -p /opt/alesc && cd /opt/alesc

# 3. Clonar o projeto do repositório oficial
sudo git clone [https://github.com/edsonbez/piloto-agente-autonomo.git](https://github.com/edsonbez/piloto-agente-autonomo.git) agente_ia

# 4. Entrar na pasta e ajustar permissões para logs e dados
cd agente_ia
sudo mkdir -p data/logs
sudo chmod -R 775 data/logs

```

## 2. Carga da Base de Conhecimento (Offline)

Os arquivos de inteligência vetorial **não residem no repositório Git** devido ao seu tamanho binário e políticas de segurança. Antes de iniciar o container, o técnico deve realizar a carga manual:

* **Arquivos Necessários:**
    * `otrs_conhecimento.index` (Índice FAISS)
    * `otrs_mapping.csv` (Base de textos expandida)

* **Procedimento:**
    Copiar ambos os arquivos para a pasta: `/opt/alesc/agente_ia/data/`

* **Permissões de Acesso:**
```bash
sudo chmod 644 /opt/alesc/agente_ia/data/*

```

## 3. Especificações de Recursos (Sizing & Performance)

* **Processamento:** 2 vCPUs (x86_64).
* **Memória RAM:** 2 GB (Limite do Container) / 4 GB (Host).
* **Memória Compartilhada (--shm-size):** **2 GB** (Obrigatório para o FAISS).
* **Armazenamento:** 20 GB SSD.
* **Rede Outbound:** Porta 443 (HTTPS) para `generativelanguage.googleapis.com`.

---

## 4. Configuração de Credenciais (.env)

O sistema utiliza um arquivo `.env` na raiz do projeto (`/opt/alesc/agente_ia/`).

* **Conteúdo Obrigatório:** `GOOGLE_API_KEY=AIzaSy...`
* **Segurança:** Sem esta chave válida, o motor ativa o **Modo de Contingência (Fallback 2511)**.

---

## 5. Estrutura de Diretórios (Padrão de Produção)

Seguindo o modelo de persistência em volume para conformidade com a LGPD:

```bash
/opt/alesc/agente_ia/
├── app.py                # Interface Streamlit
├── agente_motor.py       # Lógica da IA e Gravação de Logs
├── logica_busca.py       # Motor de busca semântica FAISS
├── database.py           # Driver de conexão MySQL
├── /data                 # VOLUME PERSISTENTE (Host)
│   ├── otrs_conhecimento.index
│   ├── otrs_mapping.csv
│   └── /logs             # Auditoria local (atendimentos.json)
├── /scripts              # Manutenção e Automação
│   └── indexador_otrs.py # Pipeline de atualização incremental
├── Dockerfile            # Receita da imagem oficial
└── DEPLOY.md             # Manual técnico de implantação

```

## 6. Instruções de Build (Dockerfile)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data/logs
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```

## 7. Comando de Execução em Produção (Docker Run)

Este comando contempla as diretrizes de segurança de rede, limites de memória e as flags de estabilidade do servidor Streamlit:

```bash
docker run -d -p 8501:8501 \
  --name agente_ia_prod \
  --env-file .env \
  -v "/opt/alesc/agente_ia/data:/app/data" \
  --shm-size=2gb \
  --restart always \
  piloto-agente-alesc \
  streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.maxMessageSize=200

```

## 8. Comandos de Manutenção (SysAdmin)

* **Verificar Status de RAM:** `docker stats agente_ia_prod`
* **Logs em Tempo Real:** `docker logs -f agente_ia_prod`
* **Atualizar Base:** Substituir arquivos em `/data` e rodar `docker restart agente_ia_prod`

