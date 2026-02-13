import pandas as pd
from datetime import datetime
from firebase_config import db
from logica_busca import verificar_saudacao, calcular_pontuacao

def executar_bateria_testes():
    testes = [
        {"tipo": "saudação", "relato": "Olá, bom dia!", "espera_saudacao": True},
        {"tipo": "ambiguidade", "relato": "SGP e pagamento", "esperado": "SGP"},
        {"tipo": "erro_digitação", "relato": "axenar pdeff", "esperado": "SGP"},
        {"tipo": "urgência", "relato": "URGENTE: meu plenarinho", "esperado": "Eventos"},
        {"tipo": "busca_vazia", "relato": "receita de bolo", "esperado_vazio": True}
    ]

    print(f"--- 🚀 INICIANDO TESTES DE ROBUSTEZ (FEVEREIRO 2026) ---")
    sucessos = 0

    for t in testes:
        print(f"\n🧪 Testando {t['tipo'].upper()}...")
        
        # 1. Validação de Saudação
        saudacao = verificar_saudacao(t['relato'])
        if t.get("espera_saudacao"):
            if saudacao:
                print("✅ Saudação identificada com sucesso.")
                sucessos += 1
                continue
        
        # 2. Validação de Lógica de Busca
        resultados = calcular_pontuacao(t['relato'])
        top_sistema = resultados[0]['sistema'] if resultados else "NADA"

        # AGORA SIM: Linha de debug funcional para vermos a ordem dos sistemas encontrados
        print(f"   🔍 Diagnóstico: Sistemas detectados -> {[r['sistema'] for r in resultados]}")

        # 3. Validação de Regras e Gravação no Firebase
        if t.get("esperado_vazio"):
            if not resultados:
                # Simula gravação de busca vazia
                db.collection('buscas_sem_sucesso').add({
                    'usuario': 'TESTE_AUTO', 'relato': t['relato'], 'data': datetime.now()
                })
                print(f"✅ Busca vazia registrada corretamente no Firebase.")
                sucessos += 1
            else:
                print(f"❌ Falhou: Deveria ser vazio mas encontrou {top_sistema}")
        
        else:
            if resultados and top_sistema == t['esperado']:
                # Simula gravação de atendimento de sucesso
                db.collection('atendimentos_web').add({
                    'servidor': 'TESTE_AUTO', 'sistema': top_sistema, 'resolvido': True, 'data': datetime.now()
                })
                print(f"✅ Sucesso: Topo é {top_sistema}. Registro enviado ao Firebase.")
                sucessos += 1
            else:
                print(f"❌ Falhou: Esperava {t['esperado']} | Encontrou: {top_sistema}")

    print(f"\n--- 📊 PLACAR FINAL: {sucessos}/5 TESTES PASSARAM ---")

if __name__ == "__main__":
    executar_bateria_testes()