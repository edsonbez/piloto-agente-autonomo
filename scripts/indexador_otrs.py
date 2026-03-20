import pymysql
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import sys

# Ajuste para importar database da pasta pai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_connection

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data") # Sobe um nível para achar a pasta data
INDEX_PATH = os.path.join(DATA_DIR, "otrs_conhecimento.index")
MAPPING_PATH = os.path.join(DATA_DIR, "otrs_mapping.csv")

print("🤖 Iniciando Indexador Incremental...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def criar_ou_atualizar_biblioteca():
    last_id = 0
    mode = 'n' # 'n' para novo, 'a' para append (incremental)

    # 1. Verifica se já existe base para ser incremental
    if os.path.exists(MAPPING_PATH):
        existing_df = pd.read_csv(MAPPING_PATH)
        if not existing_df.empty:
            last_id = int(existing_df['id'].max())
            mode = 'a'
            print(f"🔄 Modo Incremental Ativado. Último ID processado: {last_id}")

    conn = get_connection()
    
    # 2. Query Incremental: busca apenas IDs maiores que o último
    query = f"""
    SELECT 
        ticket.id, 
        ticket.title, 
        CAST(LEFT(article_data_mime.a_body, 600) AS CHAR) as a_body 
    FROM ticket
    JOIN article ON ticket.id = article.ticket_id
    JOIN article_data_mime ON article.id = article_data_mime.article_id
    WHERE ticket.id > {last_id}
    ORDER BY ticket.id ASC 
    LIMIT 50000
    """
    
    df_novos = pd.read_sql(query, conn)
    conn.close()

    if df_novos.empty:
        print("✅ Tudo atualizado! Nenhum chamado novo no OTRS.")
        return

    # 3. Processamento de Embeddings dos NOVOS dados
    df_novos['title'] = df_novos['title'].astype(str).fillna('')
    df_novos['a_body'] = df_novos['a_body'].astype(str).fillna('')
    textos = (df_novos['title'] + " " + df_novos['a_body']).tolist()
    
    print(f"🧠 Gerando mapas para {len(df_novos)} novos chamados...")
    new_embeddings = model.encode(textos, show_progress_bar=True)

    # 4. Lógica de Merge (FAISS)
    if mode == 'a':
        index = faiss.read_index(INDEX_PATH)
        index.add(np.array(new_embeddings).astype('float32'))
        # Append no CSV
        df_novos[['id', 'title', 'a_body']].to_csv(MAPPING_PATH, mode='a', header=False, index=False, encoding='utf-8')
    else:
        dimension = new_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(new_embeddings).astype('float32'))
        df_novos[['id', 'title', 'a_body']].to_csv(MAPPING_PATH, index=False, encoding='utf-8')

    # 5. Salvando Índice Final
    faiss.write_index(index, INDEX_PATH)
    print(f"💾 Base atualizada com sucesso em: {DATA_DIR}")

if __name__ == "__main__":
    criar_ou_atualizar_biblioteca()