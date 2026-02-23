# 🛡️ Piloto Agente Autônomo - Suporte ALESC

Este projeto é um assistente de IA desenvolvido para otimizar o atendimento de suporte técnico da Assembleia Legislativa de Santa Catarina (ALESC).

## 🚀 Performance Alcançada
- **Tempo médio de resposta:** ~5.5 segundos.
- **Modelo:** Google Gemini 1.5 Flash (via LangChain).
- **Base de Conhecimento:** RAG (Retrieval-Augmented Generation) com FAISS para busca semântica local.

## 🛠️ Tecnologias Utilizadas
- **Python 3.9**
- **Streamlit:** Interface de usuário.
- **Firebase:** Registro de atendimentos e monitoramento.
- **LangChain:** Orquestração da IA e Embeddings.
- **FAISS:** Busca eficiente de soluções técnicas.

## 📋 Como rodar o projeto
1. Clone o repositório.
2. Crie um arquivo `.env` com sua `GOOGLE_API_KEY`.
3. Adicione o JSON das credenciais do Firebase na raiz.
4. Instale as dependências: `pip install -r requirements.txt`.
5. Execute: `streamlit run app.py`.