from database import get_connection
import pandas as pd

def testar():
    try:
        conn = get_connection()
        print("✅ Conexão estabelecida!")
        
        # 1. Verificando quais tabelas existem
        print("\n--- Tabelas no Banco ---")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'ticket%';")
        for table in cursor.fetchall():
            print(f"Tabela encontrada: {table[0]}")
            
        # 2. Verificando se há dados na tabela ticket
        print("\n--- Contagem de Registros ---")
        cursor.execute("SELECT COUNT(*) FROM ticket;")
        total = cursor.fetchone()[0]
        print(f"Total de tickets no banco: {total}")
        
        conn.close()
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    testar()