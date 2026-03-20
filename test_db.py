from database import execute_query

def testar_conexao():
    print("🔍 Iniciando teste de conexão com o banco OTRS...")
    
    # Query para pegar os 5 chamados mais recentes que têm conteúdo
    query = """
    SELECT t.title, adm.a_body 
    FROM ticket t
    JOIN article a ON t.id = a.ticket_id
    JOIN article_data_mime adm ON a.id = adm.article_id
    WHERE t.ticket_state_id IN (2, 3)
    ORDER BY t.create_time DESC
    LIMIT 5
    """
    
    resultados = execute_query(query)
    
    if resultados:
        print(f"✅ Sucesso! Encontramos {len(resultados)} chamados.\n")
        for i, linha in enumerate(resultados, 1):
            print(f"--- Chamado #{i} ---")
            print(f"📌 ASSUNTO: {linha['title']}")
            print(f"📖 CONTEÚDO: {linha['a_body'][:150]}...") # Mostra só o início
            print("-" * 30)
    else:
        print("❌ Ops! A conexão funcionou, mas não retornou dados ou as tabelas estão vazias.")

if __name__ == "__main__":
    testar_conexao()