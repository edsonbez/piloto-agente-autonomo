import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# URL oficial para listar modelos via REST
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("--- 📡 ACESSANDO API DO GOOGLE DIRETAMENTE ---")

try:
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        modelos = dados.get('models', [])
        
        print(f"✅ Sucesso! Encontrados {len(modelos)} modelos.\n")
        
        for m in modelos:
            nome = m.get('name', 'N/A')
            metodos = m.get('supportedGenerationMethods', [])
            
            # Filtramos apenas os que servem para o Chat
            if 'generateContent' in metodos:
                print(f"⭐ MODELO: {nome}")
                print(f"   Nome Exibido: {m.get('displayName')}")
                print("-" * 40)
    else:
        print(f"❌ Erro na API: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro de conexão: {str(e)}")