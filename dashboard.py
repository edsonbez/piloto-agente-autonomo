import streamlit as st
import pandas as pd
import plotly.express as px
from firebase_config import db
from firebase_admin import firestore 
import io
from datetime import datetime

def exibir_dashboard():
    st.markdown("<h1 class='main-title'>Métricas de Eficiência e Auditoria</h1>", unsafe_allow_html=True)
    
    try:
        docs = db.collection('atendimentos_web').order_by('data', direction=firestore.Query.DESCENDING).get()
        data = [doc.to_dict() for doc in docs]
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return

    if data:
        df = pd.DataFrame(data)
        
        # KPIs principais
        total = len(df)
        resolvidos = len(df[df.get('resolvido') == True])
        autonomia = (resolvidos / total) * 100 if total > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Consultas Totais", total)
        c2.metric("Resolvidos pelo Agente", resolvidos)
        c3.metric("Taxa de Autonomia", f"{autonomia:.1f}%")

        # --- BOTÃO DE EXPORTAÇÃO COM CORREÇÃO DE TIMEZONE ---
        st.markdown("---")
        
        # Prepara o DataFrame para Excel (Remove fuso horário)
        df_export = df.copy()
        for col in df_export.columns:
            if pd.api.types.is_datetime64_any_dtype(df_export[col]) or col == 'data':
                df_export[col] = pd.to_datetime(df_export[col]).dt.tz_localize(None)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Atendimentos')
        
        st.download_button(
            label="📥 Baixar Relatório Completo (Excel)",
            data=buffer.getvalue(),
            file_name=f"Relatorio_ALESC_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Área de Gráficos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.write("### 🏢 Chamados por Sistema")
            if 'sistema' in df.columns:
                fig_pizza = px.pie(df, names='sistema', hole=0.4, 
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_pizza, use_container_width=True)

        with col_graf2:
            st.write("### 📈 Evolução Diária")
            if 'data' in df.columns:
                df['data_dia'] = pd.to_datetime(df['data']).dt.date
                df_evolucao = df.groupby('data_dia').size().reset_index(name='contagem')
                fig_linha = px.line(df_evolucao, x='data_dia', y='contagem', markers=True)
                st.plotly_chart(fig_linha, use_container_width=True)

        # Auditoria e Oportunidades
        st.markdown("---")
        st.write("### 🔍 Oportunidades de Melhoria (Buscas Vazias)")
        try:
            vazios_docs = db.collection('buscas_sem_sucesso').order_by('data', direction=firestore.Query.DESCENDING).limit(10).get()
            if vazios_docs:
                df_vazios = pd.DataFrame([d.to_dict() for d in vazios_docs])
                # Limpa data para exibição
                df_vazios['data'] = pd.to_datetime(df_vazios['data']).dt.strftime('%d/%m %H:%M')
                st.dataframe(df_vazios[['data', 'usuario', 'relato_original']], use_container_width=True)
            else:
                st.success("Nenhuma busca sem resposta registrada.")
        except:
            st.info("Coleção de buscas vazias ainda não inicializada.")

    else:
        st.info("Aguardando os primeiros atendimentos para gerar métricas.")