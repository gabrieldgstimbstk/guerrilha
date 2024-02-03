from numpy import empty
import streamlit as st
import pandas as pd
st.set_page_config(page_title='Itens Sem saldo CD',page_icon='🚩',layout='wide')

dados = pd.read_excel('relatorios_streamlit\itens_mapeados_sem_saldo_cd.xlsx')
dados['Codigo'] = dados['Codigo'].astype(str)
dados = dados.sort_values('Loja', ascending=True)
dados['Saldo CD'] = dados['Saldo CD'].astype(str)

st.title('Itens Mapeados Sem saldo CD')
st.divider()
filtros_vazio = 0

with st.container(height=430):
    st.markdown('**Filtros:**')
    with st.container(height=230):
        

        col1, col2, col3 = st.columns(3)

        # Filtros 
        lojas_selecionadas = col1.multiselect('Selecione as Lojas', dados['Loja'].unique(), placeholder='Escolha uma ou mais lojas')
        if lojas_selecionadas:
            filtros_vazio +=1
        if not lojas_selecionadas:
            lojas_selecionadas = dados['Loja'].unique()

        posicoes_selecionadas = col2.multiselect('Selecione as Posições', dados['Posição'].unique(),placeholder='Escolha uma ou mais posições')
        if posicoes_selecionadas:
            filtros_vazio +=1
        if not posicoes_selecionadas:
            posicoes_selecionadas = dados['Posição'].unique()

        moveis_selecionados = col3.multiselect('Selecione os Móveis', dados['Móvel'].unique(),placeholder='Escolha um ou mais móveis')
        if moveis_selecionados:
            filtros_vazio +=1
        if not moveis_selecionados:
            moveis_selecionados = dados['Móvel'].unique()

        compradores_selecionados = col1.multiselect('Selecione o(s) Compradore(s)', dados['Comprador'].unique(),placeholder='Escolha um ou mais Comprador')
        if compradores_selecionados:
            filtros_vazio +=1
        if not compradores_selecionados:
            compradores_selecionados = dados['Comprador'].unique()

        departamento_selecionadas = col2.multiselect('Selecione o(s) Departamento(s)', dados['Departamento'].unique(),placeholder='Escolha uma ou mais Departamento(s)')
        if departamento_selecionadas:
            filtros_vazio +=1
        if not departamento_selecionadas:
            departamento_selecionadas = dados['Departamento'].unique()


        secoes_selecionadas = col3.multiselect('Selecione as Seções', dados['Seção'].unique(),placeholder='Escolha uma ou mais Seção(ões)')
        if secoes_selecionadas:
            filtros_vazio +=1
        if not secoes_selecionadas:
            secoes_selecionadas = dados['Seção'].unique()
    

    with st.container(height=100):
        analises_selecionadas = st.multiselect('Selecione as Análises', dados['Análise'].unique(),placeholder='✅🚫⚠️🚨')
        if analises_selecionadas:
            filtros_vazio +=1
        if not analises_selecionadas:
            analises_selecionadas = dados['Análise'].unique()


df_filtrado = dados[
    (dados['Loja'].isin(lojas_selecionadas)) &
    (dados['Posição'].isin(posicoes_selecionadas)) &
    (dados['Móvel'].isin(moveis_selecionados)) &
    (dados['Análise'].isin(analises_selecionadas)) &
    (dados['Comprador'].isin(compradores_selecionados)) &
    (dados['Departamento'].isin(departamento_selecionadas)) &
    (dados['Seção'].isin(secoes_selecionadas))
]


colunas_manter = ['Loja', 'Posição', 'Móvel', 'Codigo', 'Produto', 'Saldo CD', 'Análise']

if filtros_vazio > 0:
    st.success('Você está Filtrando!',icon='✅')
    df_filtrado = df_filtrado[colunas_manter]
    st.dataframe(df_filtrado,hide_index=True,  use_container_width=True)
else:
    st.info('Por Favor, utilize o Filtro', icon='ℹ️')
    dados = dados[colunas_manter]
    st.dataframe(dados,hide_index=True,  use_container_width=True)

