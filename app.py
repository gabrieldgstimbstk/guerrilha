import streamlit as st
import pandas as pd
import plotly.express as px

# Carregue o DataFrame a partir do arquivo Excel
df = pd.read_excel('relatório_agrupado_guerrilha.xlsx')
print(df.info())

# Adicione elementos Streamlit conforme necessário
st.title('Relatório Comercial - Visualização Interativa')

# Adicione um seletor de loja para filtrar dados por loja
lojas_disponiveis = ['Rede'] + list(df['loja'].unique())
selected_loja = st.selectbox('Selecione a loja', lojas_disponiveis)

# Se "Rede" for selecionado, exibe todos os dados sem filtrar por loja
if selected_loja == 'Rede':
    filtered_df = df
else:
    filtered_df = df[df['loja'] == selected_loja]

selected_comprador = st.selectbox('Selecione o comprador', filtered_df['NOME_COMPRADOR'].unique())
filtered_df = filtered_df[filtered_df['NOME_COMPRADOR'] == selected_comprador]

filtered_df['analisar'] = filtered_df['analisar'].replace('⚠️ Atenção Expositor Maior que a venda!', '⚠️').replace('✅ Ok', '✅')

# Calcular a razão Expositor / V30 dias e ordenar a tabela por essa razão em ordem decrescente
filtered_df['razao_expositor_v30'] = filtered_df['qtd_expositor_posicao'] / filtered_df['venda_v30']
filtered_df = filtered_df.sort_values(by='razao_expositor_v30', ascending=False)

# Adicione uma tabela interativa com os dados filtrados (excluindo a coluna 'razao_expositor_v30')
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

if selected_loja == 'Rede':
    st.write(f'Dados para a {selected_loja}:')
else:
    st.write(f'Dados para a loja {selected_loja}:')

st.dataframe(filtered_df_display, hide_index=True, use_container_width=True)

# Adicione estatísticas descritivas para as vendas
st.write('Estatísticas Descritivas para Vendas:')
st.write(f'Média de Vendas: {filtered_df["Venda 30 Dias"].mean()}')
st.write(f'Mediana de Vendas: {filtered_df["Venda 30 Dias"].median()}')

# Adicione um botão para exportar os dados filtrados para CSV
if st.button('Exportar Dados para Excel'):
    filtered_df.to_excel('dados_exportados.xlsx', index=False)
    st.success('Dados exportados com sucesso!')

