from firebase_config import db
from datetime import datetime

def registrar_atendimento(nome, relato, sistema, resolvido, protocolo=None):
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

def registrar_monitoramento_ia(termo):
    """Monitora lacunas de conhecimento (ex: Erro 500) para expandir a base."""
    db.collection('monitoramento_ia').add({
        'termo_buscado': termo.lower(),
        'data': datetime.now()
    })

def registrar_busca_vazia(nome, relato):
    db.collection('buscas_sem_sucesso').add({
        'usuario': nome,
        'relato_original': relato,
        'data': datetime.now()
    })

def registrar_feedback_negativo(sistema, relato):
    db.collection('feedbacks_negativos').add({
        'sistema_rejeitado': sistema,
        'relato_usuario': relato,
        'data': datetime.now()
    })