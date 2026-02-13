import streamlit as st
import pandas as pd
from datetime import datetime
from logica_busca import verificar_saudacao, calcular_pontuacao
from dashboard import exibir_dashboard
from firebase_utils import registrar_atendimento, registrar_busca_vazia, registrar_feedback_negativo
import os

st.set_page_config(page_title="Suporte ALESC", layout="wide", page_icon="🛡️")

# Carregar CSS
if os.path.exists(os.path.join("assets", "style.css")):
    with open(os.path.join("assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Gerenciamento de Estado
if 'tentativa_atual' not in st.session_state: st.session_state.tentativa_atual = 0
if 'solucoes_encontradas' not in st.session_state: st.session_state.solucoes_encontradas = []
if 'atendimento_concluido' not in st.session_state: st.session_state.atendimento_concluido = False
if 'protocolo' not in st.session_state: st.session_state.protocolo = None
if 'form_counter' not in st.session_state: st.session_state.form_counter = 0
if 'busca_realizada' not in st.session_state: st.session_state.busca_realizada = False

def reset_atendimento():
    st.session_state.solucoes_encontradas = []
    st.session_state.tentativa_atual = 0
    st.session_state.atendimento_concluido = False
    st.session_state.protocolo = None
    st.session_state.busca_realizada = False
    st.session_state.form_counter += 1

def gerar_protocolo():
    return f"{datetime.now().strftime('%Y%m')}-{datetime.now().strftime('%H%M%S')}"

# Navegação
st.sidebar.markdown("🛡️ **ALESC DIGITAL**")
menu = st.sidebar.selectbox("Menu", ["💬 Atendimento", "📊 Gestão"])

if menu == "💬 Atendimento":
    _, col_central, _ = st.columns([1, 2, 1])
    with col_central:
        st.title("Atendimento Inteligente")
        
        if st.session_state.atendimento_concluido and st.session_state.protocolo:
            st.success(f"### Chamado Encaminhado!\n**Protocolo:** `{st.session_state.protocolo}`")
            st.info("Em breve um técnico entrará em contato.")
            if st.button("Novo Atendimento"):
                reset_atendimento()
                st.rerun()
            st.stop()

        nome = st.text_input("Seu Nome", key=f"n_{st.session_state.form_counter}")
        relato = st.text_area("Descreva o problema", key=f"r_{st.session_state.form_counter}", placeholder="Ex: Erro ao anexar no SGP...")
        
        if st.button("🔍 SOLICITAR AJUDA"):
            if nome and relato:
                saudacao = verificar_saudacao(relato)
                if saudacao:
                    st.info(saudacao)
                else:
                    resultados = calcular_pontuacao(relato)
                    st.session_state.solucoes_encontradas = resultados
                    st.session_state.busca_realizada = True
                    st.session_state.tentativa_atual = 0
                    
                    if not resultados:
                        registrar_busca_vazia(nome, relato)
            else:
                st.error("Preencha nome e relato.")

        if st.session_state.busca_realizada:
            if st.session_state.solucoes_encontradas:
                idx = st.session_state.tentativa_atual
                sugestao = st.session_state.solucoes_encontradas[idx]
                
                # --- SPOILER DE INTELIGÊNCIA ---
                if idx == 0:
                    sistemas = [s['sistema'] for s in st.session_state.solucoes_encontradas]
                    resumo = ", ".join([f"{v} de {k}" for k, v in pd.Series(sistemas).value_counts().items()])
                    st.success(f"🤖 **Análise:** Encontrei {len(sistemas)} soluções ({resumo}).")
                
                st.markdown("---")
                st.subheader(f"💡 Sugestão {idx+1} (Sistema: {sugestao['sistema']})")
                st.write(sugestao['resposta'])
                
                c1, c2, c3 = st.columns(3)
                
                if c1.button("✅ Resolveu"):
                    registrar_atendimento(nome, relato, sugestao['sistema'], True)
                    st.success("Atendimento concluído!")
                    st.balloons()
                    if st.button("Finalizar"): reset_atendimento(); st.rerun()

                if idx < len(st.session_state.solucoes_encontradas) - 1:
                    if c2.button("➡️ Outra opção"):
                        registrar_feedback_negativo(sugestao['sistema'], relato)
                        st.session_state.tentativa_atual += 1
                        st.rerun()
                
                if c3.button("📩 Chamar Técnico"):
                    prot = gerar_protocolo()
                    registrar_atendimento(nome, relato, sugestao['sistema'], False, prot)
                    st.session_state.protocolo = prot
                    st.session_state.atendimento_concluido = True
                    st.rerun()
            else:
                st.warning("⚠️ Nenhuma solução automática encontrada.")
                if st.button("📩 Enviar para o Técnico"):
                    prot = gerar_protocolo()
                    registrar_atendimento(nome, relato, "Não Identificado", False, prot)
                    st.session_state.protocolo = prot
                    st.session_state.atendimento_concluido = True
                    st.rerun()

elif menu == "📊 Gestão":
    exibir_dashboard()