import firebase_admin
from firebase_admin import credentials, firestore

# 1. Configurar as credenciais (USE O NOME DO SEU ARQUIVO JSON AQUI)
cred = credentials.Certificate("agente-helpdesk-piloto-firebase-adminsdk-fbsvc-85954069f2.json")
firebase_admin.initialize_app(cred)

# 2. Conectar ao banco de dados Firestore
db = firestore.client()

def testar_conexao():
    try:
        # Criando um chamado de teste no Firebase
        doc_ref = db.collection('chamados_piloto').document('teste_conexao')
        doc_ref.set({
            'usuario': 'Edson',
            'sistema': 'Piloto Agente ALESC',
            'status': 'Conectado com Sucesso!',
            'data': firestore.SERVER_TIMESTAMP
        })
        print("✅ Sucesso! O registro foi criado no Firestore.")
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    testar_conexao()