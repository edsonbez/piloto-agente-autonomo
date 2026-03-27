FROM python:3.10-slim

WORKDIR /app

# Dependências do sistema para FAISS e compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o necessário para instalar dependências (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte (o .dockerignore cuidará do resto)
COPY . .

# Garante a existência das pastas de volume
RUN mkdir -p /app/data/logs

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

