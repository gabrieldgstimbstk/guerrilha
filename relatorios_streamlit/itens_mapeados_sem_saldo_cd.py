import pandas as pd


# guerrilha_df = pd.read_csv('guerrilha.csv')
guerrilha_df = pd.read_excel('linkker.xlsx')

# Exposições - Cadastro de exposições
expositor_df = pd.read_csv('exp.csv', sep=';',low_memory=False)

# Mix Total - Cadastro dos itens
mix_total_df = pd.read_csv('mix_total.csv', sep=';')


guerrilha_df = guerrilha_df[['NÚMERO DA LOJA','TIPO DE PEX','NOME DO PONTO COMERCIALIZADO','SIGLA DO PONTO','Inicio','Fim','CÓDIGO SKU']]

guerrilha_df['NÚMERO DA LOJA'] = guerrilha_df['NÚMERO DA LOJA'].astype(int)

expositor_df = expositor_df[['CODIGO','DESCRICAO','DEPTO_NOME','SECAO_NOME','LOJA','SALDO_CD','QTDVENDA_30_DIAS']]

itens_map = guerrilha_df.merge(expositor_df,
                                    how='left',
                                    left_on=['CÓDIGO SKU','NÚMERO DA LOJA'],
                                    right_on=['CODIGO', 'LOJA'])

colunas = {
    'NÚMERO DA LOJA': 'Loja',
    'TIPO DE PEX': 'Nome Exposição',
    'NOME DO PONTO COMERCIALIZADO': 'Posição',
    'SIGLA DO PONTO':'Móvel',
    'CÓDIGO SKU': 'Codigo',
    'DESCRICAO': 'Produto',
    'DEPTO_NOME': 'Departamento',
    'SECAO_NOME': 'Seção',
    'SALDO_CD': 'Saldo CD',
    'QTDVENDA_30_DIAS': 'Venda 30 Dias'
}

itens_map.rename(columns=colunas, inplace=True)

itens_map = itens_map[['Loja', 'Nome Exposição', 'Posição', 'Móvel', 'Codigo', 'Produto', 'Departamento', 'Seção', 'Saldo CD', 'Venda 30 Dias']]

mix_selected = mix_total_df[['RMS','SISTEMATICA','NOME_COMPRADOR']].copy()

colunas_mix_renomear = {
    'SISTEMATICA': 'Sistematica',
    'NOME_COMPRADOR':'Comprador'
}

mix_selected.rename(columns=colunas_mix_renomear, inplace=True)

itens_mapeados = itens_map.merge(mix_selected,
                                    how='left',
                                    left_on='Codigo',
                                    right_on='RMS')


itens_mapeados.drop(columns='RMS',inplace=True)


def ajustar_formato(valor):
    if isinstance(valor, str):
        valor = valor.replace('.', '').replace(',', '.')
    return valor    


itens_mapeados['Venda 30 Dias'] = pd.to_numeric(itens_mapeados['Venda 30 Dias'].apply(ajustar_formato), errors='coerce')
itens_mapeados['Saldo CD'] = pd.to_numeric(itens_mapeados['Saldo CD'].apply(ajustar_formato), errors='coerce')

itens_mapeados['Análise'] = ''
sistematicas_validas = [1] 
moveis = ['ILHA', 'PG', 'PE']
for index, row in itens_mapeados.iterrows():
    if pd.isna(row['Produto']):
        itens_mapeados.at[index, 'Análise'] = '🚨 - Item fora de linha mapeado!'
    elif row['Sistematica'] not in sistematicas_validas:
        itens_mapeados.at[index, 'Análise'] = '🚫 - Item Sistemática Diferente de 1'
    elif row['Saldo CD'] == 0:
        itens_mapeados.at[index, 'Análise'] = '⚠️ - Item Em Ruptura no CD!'
    elif row['Móvel'] not in moveis:
        itens_mapeados.at[index, 'Análise'] = '⚠️ - Movel incopatível!'
    else:
        itens_mapeados.at[index, 'Análise'] = '✅ - Saldo CD Apto'



itens_mapeados.to_excel('relatorios_streamlit\itens_mapeados_sem_saldo_cd.xlsx',index=False)
print('Concluído ✅')