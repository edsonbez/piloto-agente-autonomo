import streamlit as st
import pandas as pd
from datetime import datetime
import time 
import os
import traceback

# Configuração da Página (DEVE ser o primeiro comando Streamlit)
st.set_page_config(page_title="Suporte ALESC", layout="wide", page_icon="🛡️")

# --- TESTE DE AMBIENTE NA BARRA LATERAL ---
st.sidebar.markdown("### 🔍 Debug de Ambiente")
if os.getenv('GOOGLE_API_KEY'):
    st.sidebar.success("✅ Chave API: Carregada")
else:
    st.sidebar.error("❌ Chave API: FALTANDO")

# Tentar importar o motor
try:
    from logica_busca import verificar_saudacao, calcular_pontuacao
    from dashboard import exibir_dashboard
    from agente_motor import consultar_ia_stream 
    st.sidebar.success("✅ Motor IA: Carregado")
except Exception as e:
    st.sidebar.error(f"💥 Erro no Motor: {str(e)}")
    st.error("Erro crítico ao carregar dependências:")
    st.code(traceback.format_exc())

# --- ESTADO DA SESSÃO ---
if 'historico_chat' not in st.session_state: st.session_state.historico_chat = ""
if 'mensagens_exibicao' not in st.session_state: st.session_state.mensagens_exibicao = []
if 'atendimento_concluido' not in st.session_state: st.session_state.atendimento_concluido = False
if 'protocolo' not in st.session_state: st.session_state.protocolo = None
if 'nome_confirmado' not in st.session_state: st.session_state.nome_confirmado = False

# Carregar CSS (Opcional)
if os.path.exists(os.path.join("assets", "style.css")):
    with open(os.path.join("assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def reset_atendimento():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def gerar_protocolo():
    return f"{datetime.now().strftime('%Y%m')}-{datetime.now().strftime('%H%M%S')}"

# --- BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **ALESC DIGITAL**")
if st.sidebar.button("🔄 Reiniciar Atendimento"): 
    reset_atendimento()

menu = st.sidebar.selectbox("Menu", ["💬 Atendimento", "📊 Gestão"])

# --- MENU: ATENDIMENTO ---
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

    if prompt := st.chat_input("Como posso ajudar?"):
        st.session_state.mensagens_exibicao.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            t_inicio = time.time() 
            
            try:
                with st.spinner("Consultando base de conhecimento ALESC..."):
                    generator = consultar_ia_stream(nome, prompt, st.session_state.historico_chat)
                    # COLETE E IMPRIMA NO TERMINAL PARA DIAGNÓSTICO
                    full_response = "".join(list(generator))
            
                    # ISSO AQUI VAI APARECER NO DOCKER LOGS SE A IA FUNCIONAR
                    print(f"\n--- DEBUG DOCKER ---")
                    print(f"✅ IA Respondeu: {full_response[:50]}...")
                    print(f"--------------------\n")
                
                # 3. Exibição final
                placeholder.markdown(full_response)
                t_fim = time.time() - t_inicio
                st.caption(f"⏱️ {t_fim:.2f}s")

                # 4. Atualização do Histórico
                if full_response.strip():
                    if "historico_chat" not in st.session_state:
                        st.session_state.historico_chat = ""
                    
                    st.session_state.historico_chat += f"\nU: {prompt}\nA: {full_response}\n"
                    st.session_state.mensagens_exibicao.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                print(f"❌ ERRO NO APP: {str(e)}")
                import traceback
                traceback.print_exc()
                st.error(f"Erro ao processar resposta: {str(e)}")

    # --- AÇÕES PÓS-RESPOSTA ---
    if st.session_state.mensagens_exibicao and not st.session_state.atendimento_concluido:
        st.markdown("---")
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button("✅ Resolveu"):
                st.success("Ficamos felizes em ajudar!")
                st.balloons()
                st.session_state.atendimento_concluido = True

        with c2:
            if st.button("📩 Chamar Técnico"):
                prot = gerar_protocolo()
                st.session_state.protocolo = prot
                st.session_state.atendimento_concluido = True
                st.rerun()

    if st.session_state.atendimento_concluido and st.session_state.protocolo:
        st.warning(f"Chamado em fila para atendimento humano. Protocolo: **{st.session_state.protocolo}**")

# --- MENU: GESTÃO ---
elif menu == "📊 Gestão":
    exibir_dashboard()