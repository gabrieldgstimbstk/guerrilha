import streamlit as st
import pandas as pd
import plotly.express as px

# Carregue o DataFrame a partir do arquivo Excel
df = pd.read_excel('Relatório_comercial_agrupado.xlsx')

# Adicione elementos Streamlit conforme necessário
st.title('Relatório Comercial - Visualização Interativa')

# Adicione um seletor de loja para filtrar dados por loja
selected_loja = st.selectbox('Selecione a Loja', df['loja'].unique())
filtered_df = df[df['loja'] == selected_loja]

# Adicione um gráfico de barras interativo para as vendas por loja
fig = px.bar(filtered_df, x='exp_nome', y='venda_30', title=f'Vendas por Loja - {selected_loja}')
st.plotly_chart(fig)

# Adicione uma tabela interativa com os dados filtrados
st.write(f'Dados para a Loja {selected_loja}:')
st.dataframe(filtered_df)

# Adicione estatísticas descritivas para as vendas
st.write('Estatísticas Descritivas para Vendas:')
st.write(f'Média de Vendas: {filtered_df["venda_30"].mean()}')
st.write(f'Mediana de Vendas: {filtered_df["venda_30"].median()}')

# Adicione um mapa interativo (supondo que você tenha colunas de Latitude e Longitude no DataFrame)
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    st.map(df[['Latitude', 'Longitude']].dropna())

# Adicione um botão para exportar os dados filtrados para CSV
if st.button('Exportar Dados para CSV'):
    filtered_df.to_csv('dados_exportados.csv', index=False)
    st.success('Dados exportados com sucesso!')
