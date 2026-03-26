Projeto de agente para atuar no primeiro nível dos chamados
Versão: 6.0 (Final - Full Spec) | Ambiente: Homologação ALESC

Responsável Técnico: Edson Bez

1. Procedimento de Aquisição do Código (Clonagem e Setup)
Para iniciar a implantação no servidor de homologação da ALESC, siga a sequência abaixo:

Bash
# 1. Navegar para o diretório de aplicações opcionais
cd /opt

# 2. Criar estrutura de diretórios da ALESC
sudo mkdir -p /opt/alesc && cd /opt/alesc

# 3. Clonar o projeto do repositório oficial
sudo git clone https://github.com/edsonbez/piloto-agente-autonomo.git agente_ia

# 4. Entrar na pasta e ajustar permissões para logs e dados
cd agente_ia
sudo mkdir -p data/logs
sudo chmod -R 775 data/logs
2. Especificações de Recursos (Sizing & Performance)
Processamento: 2 vCPUs (x86_64).

Memória RAM: 2 GB (Limite do Container) / 4 GB (Recomendado no Host).

Memória Compartilhada (--shm-size): 2 GB (Obrigatório para o FAISS).

Armazenamento: 20 GB SSD (Imagem + Base + Logs).

Rede Outbound: Porta 443 (HTTPS) para generativelanguage.googleapis.com.

Rede Inbound: Porta 8501 (TCP) para rede interna.

3. Configuração de Credenciais e Variáveis (.env)
O sistema utiliza injeção de dependências via arquivo .env na raiz do projeto (/opt/alesc/agente_ia/).

Conteúdo Obrigatório: GOOGLE_API_KEY=AIzaSy...

Segurança: Sem esta chave válida, o motor ativa automaticamente o Modo de Contingência (Fallback 2511).

4. Topologia de Diretórios e Persistência (Volumes)
A arquitetura separa a lógica de execução (Docker) dos dados de conhecimento e auditoria (Host).

Caminho Host: /opt/alesc/agente_ia/data -> Container: /app/data (Índice e CSV)

Caminho Host: /opt/alesc/agente_ia/data/logs -> Container: /app/data/logs (Auditoria)

Nota: Os arquivos .index e .csv devem estar na pasta /data do host antes da inicialização.

5. Instruções de Build (Dockerfile)
O build utiliza python:3.10-slim com suporte nativo para as bibliotecas de busca vetorial.

Dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data/logs
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
6. Comando de Execução em Produção (Docker Run)
Este comando contempla as diretrizes de segurança de rede, limites de memória e as flags de estabilidade do servidor Streamlit:

Bash
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
7. Comandos de Manutenção (SysAdmin)
Verificar Status de RAM: docker stats agente_ia_prod

Logs em Tempo Real: docker logs -f agente_ia_prod

Atualizar Base: Substituir arquivos na pasta /data do host e executar docker restart agente_ia_prod