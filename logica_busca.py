import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Configuração de Caminhos Dinâmicos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_PATH = os.path.join(DATA_DIR, "otrs_conhecimento.index")
MAPPING_PATH = os.path.join(DATA_DIR, "otrs_mapping.csv")

print("🧠 Carregando cérebro semântico...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Carregamento Seguro
index = None
df_mapping = None

if os.path.exists(INDEX_PATH) and os.path.exists(MAPPING_PATH):
    index = faiss.read_index(INDEX_PATH)
    df_mapping = pd.read_csv(MAPPING_PATH)
    print(f"✅ Biblioteca Digital carregada de: {DATA_DIR}")
else:
    print(f"❌ Erro: Arquivos não encontrados em {DATA_DIR}")

def buscar_contexto_ia(pergunta, top_k=5):
    try:
        if not pergunta or index is None:
            return "Sem contexto disponível."

        pergunta_vector = model.encode([pergunta]).astype('float32')
        distancias, indices = index.search(pergunta_vector, top_k)

        contexto = ""
        for idx in indices[0]:
            if idx != -1 and idx < len(df_mapping):
                row = df_mapping.iloc[idx]
                titulo = str(row.get('title', 'Sem Título')).strip()
                corpo = str(row.get('a_body', 'Sem Descrição')).replace('\n', ' ').strip()
                
                if titulo.lower() == "title": continue
                contexto += f"\n[HISTÓRICO REAL ALESC]\nAssunto: {titulo}\nSolução: {corpo[:500]}\n"
        
        print(f"✅ DEBUG - Chamados encontrados: {len(contexto.split('[HISTÓRICO')) - 1}")
        return contexto
    except Exception as e:
        print(f"⚠️ Erro na busca semântica: {e}")
        return ""


def verificar_saudacao(texto):
    """Verifica se o usuário apenas deu um 'oi'."""
    saudacoes = ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'ajuda']
    return any(s in texto.lower() for s in saudacoes)

def calcular_pontuacao(resposta):
    """Calcula uma pontuação baseada na qualidade da resposta (exemplo simples)."""
    if len(resposta) > 100:
        return 100
    return 50