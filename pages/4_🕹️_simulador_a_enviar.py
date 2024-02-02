import streamlit as st
import pandas as pd

st.set_page_config(page_title='Simulador de envio',
                   page_icon='🕹️',
                   layout='wide'
                   )

# Exposições - Cadastro de exposições
expositor_df = pd.read_csv('exp.csv', sep=';',low_memory=False)

# Mix Total - Cadastro dos itens
mix_total_df = pd.read_csv('mix_total.csv', sep=';')

lojas = expositor_df['LOJA'].unique()
codigos_em_linha = mix_total_df['RMS'].unique()

# Widget de seleção de códigos com multiselect
codigos_selecionados = st.multiselect('Selecione os Códigos dos produtos: ', codigos_em_linha)

# Widget de seleção do tipo de móvel com radio
moveis_disponiveis = ['PE', 'PG', 'ILHA']
movel_selecionado = st.radio('Selecione o tipo de Móvel', moveis_disponiveis, horizontal=True)

# Botão de Filtrar
filtrar_button = st.button('Filtrar')

# Criar DataFrame para armazenar os resultados finais
df_loja_movel = pd.DataFrame()

# Executar apenas se o botão "Filtrar" for clicado
if filtrar_button:
    df_itens_selecionados = mix_total_df[mix_total_df['RMS'].isin(codigos_selecionados)]

    expositor_df['CODIGO'] = expositor_df['CODIGO'].astype(str)

    for loja in lojas:
        df_temp = df_itens_selecionados.copy()
        df_temp['Móvel'] = movel_selecionado
        df_temp['Loja'] = loja

        codigo_produto = df_temp['RMS'].iloc[0]

        st.text(print(codigo_produto))
        # Mapeia as informações específicas do expositor_df com base no código do produto
        if movel_selecionado == 'ILHA':
            info_expositor = expositor_df.loc[(expositor_df['LOJA'] == loja) & (expositor_df['CODIGO'] == codigo_produto), 'ILHA_CAP'].values[0]
        elif movel_selecionado == 'PG':
            info_expositor = expositor_df.loc[(expositor_df['LOJA'] == loja) & (expositor_df['CODIGO'] == codigo_produto), 'PG_CAP'].values[0]
        elif movel_selecionado == 'PE':
            info_expositor = expositor_df.loc[(expositor_df['LOJA'] == loja) & (expositor_df['CODIGO'] == codigo_produto), 'PE_CAP'].values[0]

        # Adiciona a informação do expositor ao DataFrame
        df_temp['Info_Expositor'] = info_expositor

        df_loja_movel = pd.concat([df_loja_movel, df_temp])
    df_loja_movel['Loja'] = df_loja_movel['Loja'].astype(int)
    df_loja_movel.sort_values('Loja', ascending=True, inplace=True)

    if df_loja_movel.empty:
        st.text('Selecione Algum Filtro 👀')
    else:
        st.dataframe(df_loja_movel[['Loja','RMS', 'DESCRICAO', 'Móvel','Info_Expositor']], hide_index=True)
