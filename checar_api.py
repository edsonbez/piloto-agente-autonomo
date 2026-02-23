import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("=== DIAGNÓSTICO DE CAPACIDADE DA API (ALESC) ===")

try:
    modelos = genai.list_models()
    for m in modelos:
        print(f"\nModelo: {m.name}")
        print(f"  > Versões suportadas: {m.supported_generation_methods}")
        
    print("\n-------------------------------------------")
    print("DICA: Procure por 'generateContent' para o Chat e 'embedContent' para busca.")
except Exception as e:
    print(f"❌ Erro ao listar: {e}")