from logica_busca import buscar_contexto_ia
from database import execute_query 
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time

# Forçando o modo REST para evitar latência
os.environ["transport"] = "rest" 

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class MotorIA:
    def __init__(self):
        # Configuração do Modelo (Gemini Flash)
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest", 
            temperature=0.1,
            max_output_tokens=2000, 
            transport="rest" 
        )
        # Garante que a pasta de logs existe
        self.log_dir = os.path.join("data", "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def salvar_log_local(self, usuario, relato, resposta, tempo_exec):
        """Salva a interação em um arquivo JSON local para auditoria."""
        log_path = os.path.join(self.log_dir, "atendimentos.json")
        novo_log = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "pergunta": relato,
            "resposta": resposta,
            "performance_segundos": round(tempo_exec, 2)
        }
        
        try:
            logs = []
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
            
            logs.append(novo_log)
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log local: {e}")

    def buscar_conhecimento_otrs(self, relato):
        """Busca refinada no banco para casos específicos."""
        try:
            stopwords = ['estou', 'está', 'fazer', 'problema', 'preciso', 'ajuda']
            relato_limpo = relato.lower()
            for char in ".,?!:;()":
                relato_limpo = relato_limpo.replace(char, "")
            
            palavras = [p for p in relato_limpo.split() if len(p) > 3 and p not in stopwords]
            if not palavras: palavras = relato_limpo.split()[:2]

            filtros = " OR ".join(["t.title LIKE %s OR adm.a_body LIKE %s" for _ in palavras])
            query = f"""
            SELECT t.title, CAST(LEFT(adm.a_body, 800) AS CHAR) as a_body 
            FROM ticket t
            JOIN article a ON t.id = a.ticket_id
            JOIN article_data_mime adm ON a.id = adm.article_id
            WHERE ({filtros}) AND t.ticket_state_id IN (2, 3)
            ORDER BY t.create_time DESC LIMIT 5
            """
            
            params = []
            for p in palavras:
                params.extend([f"%{p}%", f"%{p}%"])
                
            resultados = execute_query(query, tuple(params))
            if not resultados: return "Nenhum histórico específico encontrado."
                
            contexto = ""
            for res in resultados:
                titulo = str(res.get('title', 'Sem Título'))
                corpo = str(res.get('a_body', 'Sem Conteúdo')).replace('\n', ' ').strip()
                contexto += f"\n[HISTÓRICO REAL ALESC]\nAssunto: {titulo}\nSolução: {corpo[:500]}\n"
            return contexto
        except Exception as e:
            print(f"⚠️ Erro ao acessar banco: {e}")
            return "Erro técnico ao acessar o histórico."

    def processar_atendimento_stream(self, usuario, relato, historico=""):
        inicio_atendimento = time.time()
        contexto_real = buscar_contexto_ia(relato)
        
        prompt_final = (
            f"Você é o Assistente Técnico de TI da ALESC.\n"
            f"Responda ESTRITAMENTE baseando-se no histórico abaixo.\n\n"
            f"--- HISTÓRICO REAL OTRS ---\n{contexto_real}\n\n"
            f"USUÁRIO: {usuario}\nPROBLEMA: {relato}\n\n"
            f"DIRETRIZES: 1. Anonimize nomes e gabinetes. 2. Use 'unidade administrativa'. 3. Sistema oficial é SEI. 4. Se não for TI, direcione para o setor correto."
        )
        
        try:
            print("📡 Solicitando resposta ao Gemini...")
            resposta = self.llm.invoke(prompt_final)
            full_response = getattr(resposta, 'content', str(resposta)).strip()
            
            # Salva o log localmente antes de terminar
            tempo_total = time.time() - inicio_atendimento
            self.salvar_log_local(usuario, relato, full_response, tempo_total)
            
            # ADICIONE ESTA LINHA ABAIXO PARA VOLTAR A VER NO TERMINAL:
            print(f"📊 PERFORMANCE | Total: {tempo_total:.2f}s")

            yield full_response
        except Exception as e:
            print(f"❌ Erro na IA: {str(e)}")
            yield "⚠️ Ocorreu um erro na comunicação. Tente novamente."

agente = MotorIA()

def consultar_ia_stream(usuario, relato, historico=""):
    if agente:
        for resposta_parcial in agente.processar_atendimento_stream(usuario, relato, historico):
            yield resposta_parcial
    else:
        yield "❌ Sistema de IA indisponível."