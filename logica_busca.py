from thefuzz import fuzz
from base_conhecimento import SOLUCOES_CONHECIDAS
import unicodedata
import re

def normalizar_texto(texto):
    if not texto: return ""
    texto = "".join(ch for ch in unicodedata.normalize('NFKD', texto) 
                    if unicodedata.category(ch) != 'Mn')
    return texto.lower().strip()

def detectar_urgencia(texto):
    palavras_alerta = ["urgente", "prioridade", "parado", "critico", "emergencia"]
    texto_norm = normalizar_texto(texto)
    return any(p in texto_norm for p in palavras_alerta)

def verificar_saudacao(texto):
    saudacoes = ["ola", "oi", "bom dia", "boa tarde", "boa noite", "ajuda"]
    texto_limpo = normalizar_texto(texto)
    if any(s in texto_limpo for s in saudacoes) and len(texto_limpo.split()) < 4:
        return "Olá! Sou o Assistente Virtual da ALESC. Posso ajudar com SGP, RH, Financeiro e TI."
    return None

def calcular_pontuacao(relato):
    lista_pontuada = []
    texto_usuario = normalizar_texto(relato)
    palavras_usuario = re.findall(r'\b\w+\b', texto_usuario)
    urgente = detectar_urgencia(relato)

    for item in SOLUCOES_CONHECIDAS:
        score = 0
        sistema = item['sistema'].upper()
        
        for kw_orig in item["palavras_chave"]:
            kw = normalizar_texto(kw_orig)
            
            # 1. ÂNCORA DE SIGLA (Peso imbatível)
            if kw in ["sgp", "rh", "ti", "sigef", "financeiro"]:
                if kw in palavras_usuario:
                    score += 5000 
            
            # 2. MATCH DE CONTEÚDO (Palavra inteira ou expressão)
            if kw in palavras_usuario:
                score += 500 if sistema == "SGP" else 100
            elif kw in texto_usuario and len(kw.split()) > 1:
                score += 200 if sistema == "SGP" else 80

            # 3. FUZZY CALIBRADO (Mais elástico: 65%)
            # Isso vai capturar "axenar" -> "anexar" com folga
            if len(kw) > 3:
                for p_usr in palavras_usuario:
                    if len(p_usr) < 3: continue
                    ratio = fuzz.ratio(p_usr, kw)
                    if ratio > 65: # 65% é o ponto ideal para erros grosseiros
                        score += 400 if sistema == "SGP" else 50

        if score > 0:
            if urgente: score += 100
            lista_pontuada.append({"item": item, "score": score, "sistema_nome": sistema})

    # --- FILTRO DE ROBUSTEZ: Nota de corte ---
    # Só aceita soluções com score relevante (acima de 150)
    # Isso impede que "receita de bolo" vire um chamado de TI
    solucoes_relevantes = [m for m in lista_pontuada if m['score'] >= 150]

    # Ordenação final com desempate pró-SGP
    return [m['item'] for m in sorted(solucoes_relevantes, key=lambda x: (x['score'], x['sistema_nome'] == "SGP"), reverse=True)]