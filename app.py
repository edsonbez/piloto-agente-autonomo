import streamlit as st
import pandas as pd
from datetime import datetime
import time # Importado para medir o tempo
from logica_busca import verificar_saudacao, calcular_pontuacao
from dashboard import exibir_dashboard
from firebase_utils import registrar_atendimento, registrar_monitoramento_ia
from agente_motor import consultar_ia_stream 
import os

st.set_page_config(page_title="Suporte ALESC", layout="wide", page_icon="🛡️")

# --- ESTADO DA SESSÃO ---
if 'historico_chat' not in st.session_state: st.session_state.historico_chat = ""
if 'mensagens_exibicao' not in st.session_state: st.session_state.mensagens_exibicao = []
if 'atendimento_concluido' not in st.session_state: st.session_state.atendimento_concluido = False
if 'protocolo' not in st.session_state: st.session_state.protocolo = None
if 'nome_confirmado' not in st.session_state: st.session_state.nome_confirmado = False

# Carregar CSS
if os.path.exists(os.path.join("assets", "style.css")):
    with open(os.path.join("assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def reset_atendimento():
    keys = ['atendimento_concluido', 'protocolo', 'historico_chat', 'mensagens_exibicao', 'nome_confirmado', 'user_name']
    for key in keys:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

def gerar_protocolo():
    return f"{datetime.now().strftime('%Y%m')}-{datetime.now().strftime('%H%M%S')}"

# --- BARRA LATERAL ---
st.sidebar.markdown("🛡️ **ALESC DIGITAL**")
if st.sidebar.button("🔄 Reiniciar Atendimento"): 
    reset_atendimento()
menu = st.sidebar.selectbox("Menu", ["💬 Atendimento", "📊 Gestão"])

if menu == "💬 Atendimento":
    st.title("Atendimento Inteligente ALESC")

    if not st.session_state.nome_confirmado:
        st.info("Olá! Sou o Assistente da ALESC. Como devo te chamar?")
        nome_input = st.text_input("Digite seu nome e aperte Enter", key="user_name")
        if nome_input:
            st.session_state.nome_confirmado = True
            st.rerun()
        st.stop()

    nome = st.session_state.get("user_name", "Usuário")

    for msg in st.session_state.mensagens_exibicao:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- BLOCO COM CRONÔMETRO PARA TESTE DE LENTIDÃO ---
    if prompt := st.chat_input("Como posso ajudar?"):
        st.session_state.mensagens_exibicao.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("🔍 *Conectando ao servidor de IA...*")
            
            full_response = ""
            t_inicio = time.time() # Nome curto para evitar confusão
            
            try:
                # Chama o motor
                generator = consultar_ia_stream(nome, prompt, st.session_state.historico_chat)
                
                for chunk in generator:
                    if chunk:
                        if not full_response:
                            placeholder.empty()
                        full_response += chunk
                        placeholder.markdown(full_response + " ▌")
                
                # Finaliza o texto na tela
                placeholder.markdown(full_response)
                
                # Cálculo do tempo dentro do try
                t_fim = time.time() - t_inicio
                st.caption(f"Fonte: IA | ⏱️ {t_fim:.2f}s")

                # Grava no histórico e recarrega
                if full_response.strip():
                    st.session_state.historico_chat += f"\nUsuário: {prompt}\nAssistente: {full_response}\n"
                    st.session_state.mensagens_exibicao.append({"role": "assistant", "content": full_response})
                    st.rerun()

            except Exception as e:
                st.error(f"Erro ao processar resposta: {str(e)}")



    # --- BOTÕES DE AÇÃO ---
    if st.session_state.mensagens_exibicao and not st.session_state.atendimento_concluido:
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Resolveu"):
                registrar_atendimento(nome, "Resolvido via Chat", "IA", True)
                st.success("Atendimento finalizado com sucesso!")
                st.balloons()
        with c2:
            if st.button("📩 Chamar Técnico"):
                prot = gerar_protocolo()
                relato_tecnico = st.session_state.mensagens_exibicao[-2]["content"] if len(st.session_state.mensagens_exibicao) >= 2 else prompt
                registrar_atendimento(nome, relato_tecnico, "IA", False, prot)
                st.session_state.protocolo = prot
                st.session_state.atendimento_concluido = True
                st.rerun()

    if st.session_state.atendimento_concluido:
        st.warning(f"Chamado aberto! Protocolo: **{st.session_state.protocolo}**")

elif menu == "📊 Gestão":
    exibir_dashboard()