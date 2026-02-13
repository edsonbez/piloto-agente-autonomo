import firebase_admin
from firebase_admin import credentials, firestore
from base_conhecimento import SOLUCOES_CONHECIDAS

# Inicialização (ajuste o nome do seu JSON)
if not firebase_admin._apps:
    cred = credentials.Certificate("agente-helpdesk-piloto-firebase-adminsdk-fbsvc-85954069f2.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def processar_atendimento(usuario, relato):
    relato_low = relato.lower()
    sistema = "Geral"
    autonomia = False
    sugestao = ""

    # 1. Identificação do Sistema (Lógica de Triagem)
    if any(palavra in relato_low for palavra in ["ponto", "rh", "contracheque", "férias"]):
        sistema = "RH"
    elif any(palavra in relato_low for palavra in ["processo", "assinatura", "sgp", "projeto"]):
        sistema = "Legislativo"
    elif any(palavra in relato_low for palavra in ["empenho", "financeiro", "pagamento"]):
        sistema = "Financeiro"

    # 2. Nova Lógica de Autonomia (Busca na Base de Conhecimento)
    encontrou_solucao = False
    for item in SOLUCOES_CONHECIDAS:
        # Se as palavras-chave da base estiverem no relato do usuário
        if any(p in relato_low for p in item["palavras_chave"]):
            sistema = item["sistema"]
            sugestao = item["resposta"]
            autonomia = True
            encontrou_solucao = True
            break
    
    if not encontrou_solucao:
        # Mantém a lógica de senha/acesso como padrão de segurança
        if "senha" in relato_low or "acesso" in relato_low:
            autonomia = True
            sugestao = f"Identificado problema de acesso no {sistema}. Perfil reativado via integração RH."
        else:
            sugestao = "Problema complexo identificado. Encaminhando para técnico Nível 2."

    # 3. Salvar no Firebase
    doc_ref = db.collection('atendimentos').document()
    doc_ref.set({
        'usuario': usuario,
        'relato': relato,
        'sistema': sistema,
        'resolvido_pelo_agente': autonomia,
        'resposta_agente': sugestao,
        'status': 'concluido' if autonomia else 'pendente_tecnico',
        'data': firestore.SERVER_TIMESTAMP
    })

    return f"\n🤖 AGENTE: {sugestao}"

# --- TESTE DO AGENTE ---
if __name__ == "__main__":
    nome = input("Seu nome: ")
    problema = input("Descreva o problema no sistema: ")
    print(processar_atendimento(nome, problema))