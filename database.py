import pymysql
import pymysql.cursors

def get_connection():
    """Estabelece a conexão usando PyMySQL padrão para o Pandas."""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='', 
            database='otrs',
            cursorclass=pymysql.cursors.Cursor, # Alterado para Cursor padrão
            charset='utf8mb4',
            connect_timeout=30
        )
        return connection
    except Exception as e:
        print(f"❌ Erro de conexão PyMySQL: {e}")
        return None

def execute_query(query, params=None):
    """Executa a consulta de forma segura."""
    conn = get_connection()
    if not conn: 
        return []
    try:
        # Aqui usamos o DictCursor apenas para buscas pontuais, se necessário
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"❌ Erro na consulta SQL: {e}")
        return []
    finally:
        conn.close()