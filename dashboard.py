import streamlit as st
import pandas as pd
import plotly.express as px
from firebase_config import db
from datetime import datetime  # <--- ADICIONADO: Corrige o NameError

def exibir_dashboard():
    st.title("📊 Painel de Gestão - Agente ALESC")

    # 1. Busca dados do Firebase
    atendimentos_ref = db.collection('atendimentos_web').stream()
    monitoramento_ref = db.collection('monitoramento_ia').stream()

    dados_atendimento = [doc.to_dict() for doc in atendimentos_ref]
    dados_monitoramento = [doc.to_dict() for doc in monitoramento_ref]

    if not dados_atendimento:
        st.warning("Ainda não há dados de atendimento para exibir.")
        return

    df = pd.DataFrame(dados_atendimento)
    df_monit = pd.DataFrame(dados_monitoramento)

    # --- KPIs PRINCIPAIS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total = len(df)
        st.metric("Total de Atendimentos", total)
    with col2:
        resolvidos = df[df['resolvido'] == True].shape[0]
        taxa_resolucao = (resolvidos / total) * 100 if total > 0 else 0
        st.metric("Taxa de Resolução Automática", f"{taxa_resolucao:.1f}%")
    with col3:
        gaps = len(df_monit)
        st.metric("Intervenções da IA", gaps)

    st.markdown("---")

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Sistemas com Mais Chamados")
        fig_sistema = px.pie(df, names='sistema', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_sistema, width='stretch') # Atualizado conforme aviso do Streamlit

    with c2:
        st.subheader("Top 10 Dúvidas na IA")
        if not df_monit.empty:
            top_termos = df_monit['termo_buscado'].value_counts().reset_index()
            top_termos.columns = ['Termo', 'Frequência']
            
            fig_barras = px.bar(top_termos.head(10), x='Frequência', y='Termo', 
                               orientation='h', color='Frequência', color_continuous_scale='Viridis')
            st.plotly_chart(fig_barras, width='stretch')
        else:
            st.info("Nenhum dado de monitoramento capturado.")

    # --- TABELA DE DETALHES ---
    st.markdown("---")
    st.subheader("📋 Detalhes dos Atendimentos")
    # Organiza a tabela
    if 'data' in df.columns:
        df = df.sort_values(by='data', ascending=False)
    
    st.dataframe(df, width='stretch')

    # Botão de Exportação
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Relatório Completo (CSV)",
        data=csv,
        file_name=f"relatorio_alesc_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime='text/csv',
    )