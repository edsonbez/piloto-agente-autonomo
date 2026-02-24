import streamlit as st
import pandas as pd
import plotly.express as px
from firebase_config import db
from datetime import datetime

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
        # Garantindo que a coluna 'resolvido' seja tratada corretamente
        resolvidos = df[df['resolvido'] == True].shape[0] if 'resolvido' in df.columns else 0
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
        # Gráfico de Pizza focado no campo 'sistema'
        if 'sistema' in df.columns:
            fig_sistema = px.pie(df, names='sistema', hole=0.4, 
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_sistema, use_container_width=True)
        else:
            st.info("Coluna 'sistema' não encontrada nos dados.")

    with c2:
        st.subheader("Volume por Sistema (Gráfico de Barras)")
        # AJUSTE AQUI: Em vez de mostrar a frase (termo), mostramos o SISTEMA agrupado
        if 'sistema' in df.columns:
            contagem_sistema = df['sistema'].value_counts().reset_index()
            contagem_sistema.columns = ['Sistema', 'Qtd']
            
            fig_barras = px.bar(contagem_sistema.head(10), x='Qtd', y='Sistema', 
                                orientation='h', 
                                color='Qtd', 
                                color_continuous_scale='Blues',
                                labels={'Qtd': 'Nº de Atendimentos'})
            
            # Ajuste de layout para evitar nomes cortados
            fig_barras.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_barras, use_container_width=True)
        else:
            st.info("Dados de sistemas insuficientes para gerar barras.")

    # --- TABELA DE DETALHES ---
    st.markdown("---")
    st.subheader("📋 Detalhes dos Atendimentos")
    
    # Organiza a tabela pela data se existir
    if 'data' in df.columns:
        df = df.sort_values(by='data', ascending=False)
    
    # Selecionamos apenas colunas úteis para a tabela não ficar gigante
    colunas_exibir = [c for c in ['data', 'usuario', 'sistema', 'relato', 'resolvido'] if c in df.columns]
    st.dataframe(df[colunas_exibir], use_container_width=True)

    # Botão de Exportação
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Relatório Completo (CSV)",
        data=csv,
        file_name=f"relatorio_alesc_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime='text/csv',
    )