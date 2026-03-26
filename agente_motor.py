from logica_busca import buscar_contexto_ia, verificar_saudacao
from database import execute_query 
import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv
import time
import re

# Força o Python a liberar o print no terminal do Docker imediatamente
sys.stdout.reconfigure(line_buffering=True)

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

    def limpar_texto_otrs(self, texto):
        """
        Limpeza conservadora: remove apenas HTML e normaliza o texto.
        PRESERVA LINKS E CONTEÚDO TÉCNICO.
        """
        if not texto: return ""
        
        # 1. Remove tags HTML (sujeira de banco de dados/e-mail)
        texto = re.sub(r'<.*?>', '', texto)
        
        # 2. Remove saudações e assinaturas comuns para focar na solução
        regras_limpeza = [
            r"(?i)atenciosamente.*", r"(?i)cordialmente.*", 
            r"(?i)bom dia.*", r"(?i)boa tarde.*", r"(?i)boa noite.*",
            r"(?i)enviado do meu.*"
        ]
        for regra in regras_limpeza:
            texto = re.sub(regra, '', texto, flags=re.DOTALL)
            
        # 3. Normaliza espaços e quebras de linha (deixa o texto contínuo)
        texto = re.sub(r'\s+', ' ', texto)
        
        # 4. Limite de segurança por chamado (ajustado para 1000 para não cortar links longos)
        return texto[:1000].strip()

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
                    try: logs = json.load(f)
                    except: logs = []
            
            logs.append(novo_log)
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log local: {e}")

    def processar_atendimento_stream(self, usuario, relato, historico=""):
        inicio_atendimento = time.time()
        
        # --- 1. FILTRO DE SAUDAÇÃO ---
        if verificar_saudacao(relato) and len(relato.split()) < 4:
            yield f"Olá {usuario}! Sou o Assistente de TI da ALESC. Como posso ajudar com os sistemas da Casa hoje?"
            return

        # --- 2. BUSCA E LIMPEZA DE CONTEXTO ---
        print(f"\n🔍 [DEBUG 1] Iniciando busca de contexto...")
        try:
            contexto_bruto = buscar_contexto_ia(relato, top_k=5)
            
            if isinstance(contexto_bruto, list):
                contexto_limpo = [self.limpar_texto_otrs(c) for c in contexto_bruto]
                contexto_real = "\n---\n".join(contexto_limpo)
            else:
                contexto_real = self.limpar_texto_otrs(contexto_bruto)

            print("\n--- [DEBUG 2.5] CONTEXTO ENVIADO (HTML REMOVIDO / LINKS PRESERVADOS) ---")
            print(contexto_real[:500] + "...") 
            print("--- FIM DO CONTEXTO ---\n")

        except Exception as e:
            print(f"❌ [DEBUG ERRO BUSCA]: {str(e)}")
            contexto_real = "Erro ao buscar contexto técnico."

        # --- 3. PROMPT REFINADO ---
        RAMAL_OFICIAL = "2511"
        prompt_final = (
            f"Você é o Assistente Técnico de TI da ALESC. Use o HISTÓRICO abaixo e os DADOS MESTRES.\n\n"
            f"--- DADOS MESTRES (VERDADE ABSOLUTA) ---\n"
            f"- O ramal oficial do suporte de TI é: {RAMAL_OFICIAL}\n"
            f"- SEMPRE use este ramal ao direcionar o usuário para o suporte por telefone.\n\n"
            f"--- HISTÓRICO REAL OTRS ---\n{contexto_real}\n\n"
            f"REGRAS DE OURO:\n"
            f"1. PROIBIDO inventar qualquer outro número de ramal. Use apenas o {RAMAL_OFICIAL}.\n"
            f"2. Se o problema for senha do SEI, foque no procedimento de troca de senha de rede da ALESC.\n"
            f"3. Responda de forma técnica, direta e educada.\n\n"
            f"USUÁRIO: {usuario}\n"
            f"PROBLEMA: {relato}\n\n"
            f"RESPOSTA TÉCNICA FORMATADA:"
        )
        
        try:
            print("📡 [DEBUG 3] Solicitando resposta ao Gemini...")
            resposta = self.llm.invoke(prompt_final)
            
            if hasattr(resposta, 'content'):
                conteudo = resposta.content
                if isinstance(conteudo, list) and len(conteudo) > 0:
                    item = conteudo[0]
                    full_response = item.get('text', str(item)) if isinstance(item, dict) else str(item)
                else:
                    full_response = str(conteudo)
            else:
                full_response = str(resposta)

            full_response = full_response.strip()
            
            tempo_total = time.time() - inicio_atendimento
            self.salvar_log_local(usuario, relato, full_response, tempo_total)
            
            yield full_response

        except Exception as e:
            print(f"❌ [DEBUG ERRO IA]: {str(e)}")
            erro_str = str(e).lower()
            if "429" in erro_str or "resource_exhausted" in erro_str:
                yield f"⚠️ **Alta Demanda:** No momento estou processando muitas solicitações. Entre em contato com o suporte pelo **ramal {RAMAL_OFICIAL}**."
            else:
                yield f"⚠️ **Erro técnico:** Tivemos uma oscilação. Por favor, tente novamente ou ligue no **ramal {RAMAL_OFICIAL}**."

agente = MotorIA()

def consultar_ia_stream(usuario, relato, historico=""):
    global agente
    try:
        if agente:
            for resposta_parcial in agente.processar_atendimento_stream(usuario, relato, historico):
                yield resposta_parcial
        else:
            yield "❌ Sistema de IA indisponível."
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {str(e)}")
        yield f"⚠️ Erro técnico: {str(e)}"