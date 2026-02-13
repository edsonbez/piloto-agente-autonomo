import firebase_admin
from firebase_admin import credentials, firestore

def init_db():
    if not firebase_admin._apps:
        # Certifique-se de que o nome do arquivo .json está correto
        cred = credentials.Certificate("agente-helpdesk-piloto-firebase-adminsdk-fbsvc-85954069f2.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_db()