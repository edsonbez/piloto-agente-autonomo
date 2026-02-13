from firebase_config import db
from datetime import datetime

def registrar_atendimento(nome, relato, sistema, resolvido, protocolo=None):
    """Registra atendimentos resolvidos ou encaminhados ao técnico."""
    dados = {
        'servidor': nome,
        'problema': relato,
        'sistema': sistema,
        'resolvido': resolvido,
        'data': datetime.now()
    }
    if protocolo:
        dados['protocolo'] = protocolo
    
    db.collection('atendimentos_web').add(dados)

def registrar_busca_vazia(nome, relato):
    """Registra relatos que não geraram nenhuma sugestão automática."""
    db.collection('buscas_sem_sucesso').add({
        'usuario': nome,
        'relato_original': relato,
        'data': datetime.now()
    })

def registrar_feedback_negativo(sistema, relato):
    """Registra quando o usuário pula uma sugestão."""
    db.collection('feedbacks_negativos').add({
        'sistema_rejeitado': sistema,
        'relato_usuario': relato,
        'data': datetime.now()
    })