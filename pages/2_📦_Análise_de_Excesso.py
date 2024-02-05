from numpy import place
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Análise Excesso',
                   page_icon='📦',
                   layout='wide'
)


df = pd.read_excel('relatório_agrupado_guerrilha.xlsx')

lojas_disponiveis =list(df['loja'].unique())

selected_loja = st.multiselect('Selecione a Loja', lojas_disponiveis, placeholder='Selecione uma ou mais Lojas')

if not selected_loja:
    filtered_df = df
else:
    if selected_loja:
        if 'Rede' in selected_loja:
            filtered_df = df
        else:
            filtered_df = df[df['loja'].isin(selected_loja)]


compradores_disponiveis = ['Todos Compradores'] + list(df['NOME_COMPRADOR'].unique())
selected_comprador = st.selectbox('Selecione o comprador', compradores_disponiveis)

if selected_comprador != 'Todos Compradores':
    filtered_df = filtered_df[filtered_df['NOME_COMPRADOR'] == selected_comprador]

tipo_analisar = st.multiselect(
    'Selecione a Análise',
    list(filtered_df['analisar'].unique())
)


if tipo_analisar:
    filtered_df = filtered_df[filtered_df['analisar'].isin(tipo_analisar)]
# filtered_df['analisar'] = filtered_df['analisar'].replace('⚠️ Atenção Expositor Maior que a venda!', '⚠️').replace('✅ Ok', '✅')

filtered_df['razao_expositor_v30'] = filtered_df['qtd_expositor_posicao'] / filtered_df['venda_v30']
filtered_df = filtered_df.sort_values(by='razao_expositor_v30', ascending=False)


filtered_df_display = filtered_df[['loja', 'codigo_sku', 'DESCRICAO', 'venda_v30', 'qtd_expositor_posicao', 'analisar']]
filtered_df_display['codigo_sku'] = filtered_df_display['codigo_sku'].astype(str)
colunas_renomear = {
    'loja': 'Loja',
    'codigo_sku': 'Código',
    'DESCRICAO': 'Produto',
    'venda_v30': 'V30 dias',
    'qtd_expositor_posicao': 'Expositor',
    'analisar': 'Análise',
}

filtered_df_display.rename(columns=colunas_renomear, inplace=True)

if len(selected_loja) > 0:
    st.write(f'Dados para a loja {", ".join(map(str, selected_loja))}:')

    

st.dataframe(filtered_df_display, hide_index=True, use_container_width=True)


if st.button('Exportar Dados para Excel'):
    filtered_df.to_excel('dados_exportados.xlsx', index=False)
    st.success('Dados exportados com sucesso!')