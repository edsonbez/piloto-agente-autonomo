import firebase_admin
from firebase_admin import credentials, firestore
from base_conhecimento import SOLUCOES_CONHECIDAS
import os
from dotenv import load_dotenv
import time

# Forçando o modo REST para evitar latência
os.environ["transport"] = "rest" 

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

# Inicialização segura do Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("agente-helpdesk-piloto-firebase-adminsdk-fbsvc-85954069f2.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

class MotorIA:
    def __init__(self):
        # 1. Base de conhecimento para o FAISS
        self.documentos = [
            Document(
                page_content=f"Sistema: {item['sistema']}. Problema: {' '.join(item['palavras_chave'])}. Resposta: {item['resposta']}",
                metadata={"sistema": item['sistema'], "resposta": item['resposta']}
            ) for item in SOLUCOES_CONHECIDAS
        ]
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vectorstore = FAISS.from_documents(self.documentos, self.embeddings)
        
        # 2. Configuração do Modelo (Gemini Flash)
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest", 
            temperature=0.1,
            max_output_tokens=800,
            max_retries=0, 
            transport="rest" 
        )

    def processar_atendimento_stream(self, usuario, relato, historico=""):
        inicio_atendimento = time.time()
        
        # Busca Semântica
        docs = self.vectorstore.similarity_search(relato, k=1)
        contexto = docs[0].page_content if docs else "Geral"
        
        prompt_final = (
            f"Aja como suporte técnico nível 2. Use o CONTEXTO: {contexto}\n"
            f"PERGUNTA: {relato}\n"
            f"INSTRUÇÃO: Vá DIRETO AOS PASSOS TÉCNICOS. Sem saudações."
        )
        
        try:
            print("📡 Solicitando resposta ao Google...")
            resposta = self.llm.invoke(prompt_final)
            full_response = getattr(resposta, 'content', str(resposta))
            full_response = full_response.replace("content=", "").strip("'\"")
            yield full_response

        except Exception as e:
            print(f"❌ Erro na IA: {str(e)}")
            yield f"\n⚠️ Ocorreu um erro na comunicação. Tente novamente."

        tempo_final_calculado = time.time() - inicio_atendimento
        print(f"📊 PERFORMANCE | Total: {tempo_final_calculado:.2f}s")

# Instância global
try:
    agente = MotorIA()
except Exception as e:
    agente = None

def consultar_ia_stream(usuario, relato, historico=""):
    if agente:
        for resposta_parcial in agente.processar_atendimento_stream(usuario, relato, historico):
            if resposta_parcial:
                yield resposta_parcial
    else:
        yield "❌ Sistema de IA indisponível."