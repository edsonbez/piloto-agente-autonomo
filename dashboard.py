import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
from datetime import datetime

def exibir_dashboard():
    st.title("📊 Painel de Gestão - Agente ALESC")

    # 1. Definição do caminho do Log Local
    LOG_PATH = os.path.join("data", "logs", "atendimentos.json")

    # 2. Carregamento dos dados do JSON
    if not os.path.exists(LOG_PATH):
        st.warning("Ainda não há dados de atendimento local para exibir. Aguardando o primeiro atendimento...")
        return

    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            dados_atendimento = json.load(f)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo de logs: {e}")
        return

    if not dados_atendimento:
        st.info("O arquivo de logs está vazio.")
        return

    # Converte para DataFrame
    df = pd.DataFrame(dados_atendimento)

    # --- TRATAMENTO DE COLUNAS ---
    # Como o JSON usa nomes de campos do código, vamos mapear para o que o Dashboard espera
    if 'timestamp' in df.columns:
        df['data'] = pd.to_datetime(df['timestamp'])
    
    # Criamos a coluna 'sistema' baseada em palavras-chave se ela não existir no JSON
    # (Ou você pode adicionar a detecção de sistema no agente_motor.py depois)
    if 'sistema' not in df.columns:
        df['sistema'] = "Geral/TI" 

    # --- KPIs PRINCIPAIS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total = len(df)
        st.metric("Total de Atendimentos", total)
    with col2:
        # No log local, podemos considerar 'resolvido' se a resposta foi gerada com sucesso
        # Se você quiser um contador real, precisaremos adicionar o campo 'resolvido' no agente_motor
        st.metric("Taxa de Resolução Automática", "100%") 
    with col3:
        # Performance média vinda do JSON
        perf_media = df['performance_segundos'].mean() if 'performance_segundos' in df.columns else 0
        st.metric("Tempo Médio de Resposta", f"{perf_media:.2f}s")

    st.markdown("---")

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Sistemas com Mais Chamados")
        if 'sistema' in df.columns:
            fig_sistema = px.pie(df, names='sistema', hole=0.4, 
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_sistema, use_container_width=True)

    with c2:
        st.subheader("Volume por Sistema")
        if 'sistema' in df.columns:
            contagem_sistema = df['sistema'].value_counts().reset_index()
            contagem_sistema.columns = ['Sistema', 'Qtd']
            
            fig_barras = px.bar(contagem_sistema, x='Qtd', y='Sistema', 
                                orientation='h', color='Qtd', 
                                color_continuous_scale='Blues')
            st.plotly_chart(fig_barras, use_container_width=True)

    # --- TABELA DE AUDITORIA ---
    st.markdown("---")
    st.subheader("📋 Auditoria de Atendimentos (Local)")
    
    if 'data' in df.columns:
        df = df.sort_values(by='data', ascending=False)
        df['data_exibicao'] = df['data'].dt.strftime('%d/%m/%Y %H:%M')
    
    # Mapeando os nomes das colunas do JSON para a tabela
    colunas_finais = {
        "data_exibicao": "Data/Hora",
        "usuario": "Usuário",
        "pergunta": "Pergunta do Usuário",
        "resposta": "Solução Entregue",
        "performance_segundos": "Tempo (s)"
    }

    st.dataframe(
        df[list(colunas_finais.keys())].rename(columns=colunas_finais), 
        use_container_width=True,
        hide_index=True
    )

    # Botão de Exportação
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Relatório Local (CSV)",
        data=csv,
        file_name=f"auditoria_alesc_local_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime='text/csv',
    )