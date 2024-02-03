import streamlit as st
import pandas as pd
st.set_page_config(page_title='Itens Sem saldo CD',page_icon='🚩',layout='wide')

dados = pd.read_excel('relatorios_streamlit\itens_mapeados_sem_saldo_cd.xlsx')
dados['Codigo'] = dados['Codigo'].astype(str)


st.title('Itens Mapeados Sem saldo CD')



colunas_manter = ['Loja', 'Posição', 'Móvel', 'Codigo', 'Produto', 'Saldo CD', 'Análise']
df_filtrado = dados[colunas_manter]
st.dataframe(df_filtrado,  use_container_width=True)


