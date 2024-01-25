# Importando as Blibliotecas
import pandas as pd
import warnings

# Ignorar todos os UserWarnings
warnings.simplefilter("ignore", UserWarning)

# Importando os dados

# Planilha linkker
linkker_df = pd.read_excel('linkker.xlsx')

# Planilha das exposições
expositor_df = pd.read_csv('exp.csv', sep=';')

# Mix total
mix_total_df = pd.read_csv('mix_total.csv', sep=';')

# Cadastro de usuário do abastecimento - Informação do analista responsável no abastecimento por departamento e seção
usuario_abastecimento = pd.read_excel('cadastro_usuario_abastecimento.xlsx')

# Limpando a planilha Linkker



lojas_validas = [51, 108, 116, 124, 167, 175, 183, 205, 230, 248, 264, 272, 310, 329, 337]  # Loja sem regra de corte
posicoes_compativeis = ['PE', 'PG', 'ILHA']
em_linha = mix_total_df['RMS']

linkker_df['NÚMERO DA LOJA'] = linkker_df['NÚMERO DA LOJA'].astype(int)

linkker_df = linkker_df[
    (linkker_df['NÚMERO DA LOJA'].isin(lojas_validas)) &  # Verifica se o produto está em linha
    (linkker_df['SIGLA DO PONTO'].isin(posicoes_compativeis)) &  # Verifica se a NOME DO PONTO COMERCIALIZADO é valida
    (~linkker_df['CÓDIGO SKU'].isnull()) &  # Verifica se o campo código está vazio
     (linkker_df['CÓDIGO SKU'].isin(em_linha))  # Verifica se o produto está em linha (na rede)
    ]




# Retira as colunas que não vai ser útil para essa análise
colunas_manter = ['NÚMERO DA LOJA', 'TIPO DE PEX', 'NOME DO PONTO COMERCIALIZADO', 'SIGLA DO PONTO', 'Inicio', 'Fim',
                  'DATA DA VENDA', 'TIPO DE PERÍODO', 'USER QUE VENDEU', 'NOME SKU', 'CÓDIGO SKU']
linkker_df = linkker_df.loc[:, colunas_manter]

# Limpando e ajustando o DataFrame exp_df

def ajustar_formato(valor):
    if isinstance(valor, str):
        valor = valor.replace('.', '').replace(',', '.')
    return valor


# Aplicando a função na coluna QTDVENDA_30_DIAS
expositor_df['QTDVENDA_30_DIAS'] = expositor_df['QTDVENDA_30_DIAS'].apply(ajustar_formato)

# Convertendo a coluna para o tipo numérico
expositor_df['QTDVENDA_30_DIAS'] = pd.to_numeric(expositor_df['QTDVENDA_30_DIAS'], errors='coerce')

colunas_manter = ['CODIGO', 'LOJA', 'ILHA_CAP', 'PE_CAP', 'PG_CAP', 'SALDO_CD', 'QTDVENDA_30_DIAS']

exp_df = expositor_df.loc[:, colunas_manter]

# Renomeando as colunas do DF


column_mapping = {
    'CODIGO': 'codigo',
    'NÚMERO DA LOJA': 'loja',
    'ILHA_CAP': 'ilha',
    'PE_CAP': 'pe',
    'PG_CAP': 'pg',
    'QTDVENDA_30_DIAS': 'venda_30',
    'SALDO_CD': 'saldo_cd',

}

exp_df.rename(columns=column_mapping, inplace=True)

lkr_cols = linkker_df.columns  # Visualizar as colunas da linkker, como ficou após limpar a base
exp_cols = exp_df.columns  # Visualizar as colunas dos expositores, e conferir com a linkker

print('Colunas expositor: ', exp_cols)
print('Colunas linkker: ', lkr_cols)

print(f'{exp_df.shape=}')
print(f'{linkker_df.shape=}')



linkker_df['Inicio'].dtypes

# teste resolução
# Merge exp_df with linkker_df based on 'NÚMERO DA LOJA' and 'CÓDIGO SKU'
merged_df = linkker_df.merge(exp_df[['LOJA', 'codigo', 'venda_30', 'pe', 'pg', 'ilha', 'saldo_cd']],
                             left_on=['NÚMERO DA LOJA', 'CÓDIGO SKU'],
                             right_on=['LOJA', 'codigo'],
                             how='left')


# Copy the 'venda_30' values from merged_df to linkker_df
linkker_df['venda_30'] = merged_df['venda_30']

# Selecionar as colunas relevantes após a junção
result_df = merged_df[
    ['NÚMERO DA LOJA', 'TIPO DE PEX', 'Inicio', 'Fim', 'DATA DA VENDA', 'TIPO DE PERÍODO',
     'USER QUE VENDEU', 'NOME DO PONTO COMERCIALIZADO', 'SIGLA DO PONTO', 'NOME SKU', 'CÓDIGO SKU', 'venda_30', 'pe', 'pg', 'ilha', 'saldo_cd']].copy()

# preencher os valores vazios por zero

result_df['venda_30'] = result_df['venda_30'].fillna(0)

# Ajustando tipos de colunas
result_df.loc[:, 'pe'] = result_df['pe'].astype(float)
result_df.loc[:, 'pg'] = result_df['pg'].astype(float)
result_df.loc[:, 'ilha'] = result_df['ilha'].astype(float)
result_df.loc[:, 'saldo_cd'] = result_df['saldo_cd'].astype(float)

# Converter a coluna 'venda_30' para float
result_df['venda_30'] = result_df['venda_30'].astype(float)

# Filtrar o DataFrame para manter apenas as linhas onde 'saldo_cd' é maior que 1
result_df_filtrado = result_df[result_df['saldo_cd'] > 1]

# Agrupar e somar as Vendas por 'NÚMERO DA LOJA' e 'NOME DO PONTO COMERCIALIZADO'
agrup_soma_vda_loja_posicao = result_df_filtrado.groupby(['NÚMERO DA LOJA', 'NOME DO PONTO COMERCIALIZADO'])['venda_30'].sum().reset_index()

# Fazendo o merge com o DataFrame original
result_df = pd.merge(result_df, agrup_soma_vda_loja_posicao, on=['NÚMERO DA LOJA', 'NOME DO PONTO COMERCIALIZADO'], how='left')

# ---------------------------
# Chave de pesquisa entre o DF mix_total e result_df
chave_mix = 'RMS'
chave_result = 'CÓDIGO SKU'

# Colunas a serem selecionadas do mix_total_df
colunas_selecionadas_mix = ['DESCRICAO','SISTEMATICA', 'NOME_COMPRADOR', 'NOME_DEPARTAMENTO', 'SECAO', 'NOME_SECAO']

# Procura no mix total as colunas sistemática, nome do comprador, nome do departamento, seção, nome da seção e adiciona no DataFrame
result_df = result_df.merge(mix_total_df[colunas_selecionadas_mix + [chave_mix]],
                            how='left',
                            left_on=chave_result,
                            right_on=chave_mix)

# Remover a coluna utilizada como chave

result_df.drop(columns=[chave_mix], inplace=True)

# Valida e deixa somente os itens que são sistemática 1



sistematica_validas = [1]

result_df = result_df[result_df['SISTEMATICA'].isin(sistematica_validas)]

# Renomeando as colunas do DF


column_mapping = {
    'NÚMERO DA LOJA': 'loja',
    'venda_30_y': 'soma_venda_posicao',
    'venda_30_x': 'venda_30',
    'TIPO DE PEX': 'exp_nome',
    'Inicio': 'dt_inicio',
    'Fim': 'dt_fim',
    'TIPO DE PERÍODO': 'tipo_periodo',
    'USER QUE VENDEU': 'user_log',
    'DATA DA VENDA': 'dt_log',
    'NOME DO PONTO COMERCIALIZADO': 'posicao_movel',
    'SIGLA DO PONTO': 'tipo_movel',
    'DESCRICAO': 'nome_sku',
    'CÓDIGO SKU': 'codigo_sku',
    'SISTEMATICA': 'sistematica',
    'NOME_COMPRADOR': 'comprador',
    'NOME_DEPARTAMENTO': 'departamento',
    'SECAO': 'secao_id',
    'NOME_SECAO': 'secao'
}

result_df.rename(columns=column_mapping, inplace=True)

result_df['ilha'] = result_df['ilha'].fillna(0)
result_df['pg'] = result_df['pg'].fillna(0)
result_df['pe'] = result_df['pe'].fillna(0)




def map_capacidade(row):
    if row['tipo_movel'] == 'ILHA':
        return row['ilha']
    elif row['tipo_movel'] == 'PG':
        return row['pg']
    elif row['tipo_movel'] == 'PE':
        return row['pe']
    else:
        return None


result_df['capac_movel_mapeado'] = result_df.apply(map_capacidade, axis=1)





# Analisar os Produtos na Loja x NOME DO PONTO COMERCIALIZADO que não tem Exposição cadastrada

# Filtra os itens mapeados sem cadastro de expositor
itens_sem_exposicao_df = result_df[result_df['capac_movel_mapeado'] == 0].copy()

# Atribui um analista de abastecimento correspondente por seção
itens_sem_exposicao_df = itens_sem_exposicao_df.merge(usuario_abastecimento[['secao_id', 'analista_abastecimento']],
                                                      on='secao_id', how='left')

# Remover linhas com valores NaN na coluna 'analista_abastecimento' - ou seja é um departamento que não é vai volume na linkker
# pelo abastecimento pelos parâmetros cadastrados na planilha usuario_abastecimento

itens_sem_exposicao_df = itens_sem_exposicao_df.dropna(subset=['analista_abastecimento'])

# Retira as colunas que não vai ser útil para essa análise

colunas_manter_exp = ['departamento', 'secao', 'loja', 'codigo_sku', 'nome_sku', 'posicao_movel', 'tipo_movel',
                      'capac_movel_mapeado', 'analista_abastecimento']
itens_sem_exposicao_df = itens_sem_exposicao_df.loc[:, colunas_manter_exp]

# Criar um arquivo Excel
nome_arquivo_excel = "Relatorio_itens_sem_expositor_cadastrado.xlsx"
writer = pd.ExcelWriter(nome_arquivo_excel, engine='xlsxwriter')

# Salvar cada DataFrame em uma planilha separada
analistas = itens_sem_exposicao_df['analista_abastecimento'].unique()

for analista in analistas:
    analista_df = itens_sem_exposicao_df[itens_sem_exposicao_df['analista_abastecimento'] == analista]
    analista_df.to_excel(writer, sheet_name=analista, index=False)

# Fechar o arquivo Excel
writer.close()

print(f"Arquivo {nome_arquivo_excel} exportado com sucesso.")

# Tirar itens com saldo CD < 1
colunas_manter = ['loja', 'exp_nome', 'dt_inicio', 'dt_fim', 'dt_log', 'tipo_periodo', 'user_log', 'posicao_movel',
                  'tipo_movel', 'nome_sku', 'codigo_sku', 'venda_30', 'pe', 'pg', 'ilha', 'saldo_cd',
                  'soma_venda_posicao', 'sistematica', 'comprador', 'departamento', 'secao_id', 'secao',
                  'capac_movel_mapeado']


linhas = result_df['saldo_cd'] > 1
result_df = result_df.loc[linhas, colunas_manter]


# Tirar itens com venda_30 0
colunas_manter = ['loja', 'exp_nome', 'dt_inicio', 'dt_fim', 'dt_log', 'tipo_periodo', 'user_log', 'posicao_movel',
                  'tipo_movel', 'nome_sku', 'codigo_sku', 'venda_30', 'pe', 'pg', 'ilha', 'saldo_cd',
                  'soma_venda_posicao', 'sistematica', 'comprador', 'departamento', 'secao_id', 'secao',
                  'capac_movel_mapeado']
linhas = result_df['venda_30'] > 0

result_df = result_df.loc[linhas, colunas_manter]

# Criar uma nova coluna 'qtd_exp_calc' inicialmente preenchida com zeros
result_df['qtd_exp_calc_posicao'] = 0

# Iterar pelas linhas do DataFrame para calcular os valores da nova coluna
for index, row in result_df.iterrows():
    venda_30 = row['venda_30']
    soma_venda_posicao = row['soma_venda_posicao']
    capac_movel_mapeado = row['capac_movel_mapeado']
    saldo_cd = row['saldo_cd']  # Adicionar esta linha para obter o valor de saldo_cd

    if saldo_cd > 1:  # Verificar se o saldo_cd é maior que 1
        if soma_venda_posicao != 0:
            qtd_exp_temp = (venda_30 / soma_venda_posicao) * capac_movel_mapeado
            result_df.at[index, 'qtd_exp_calc_posicao'] = qtd_exp_temp

result_df['qtd_exp_calc_total'] = result_df.groupby(['loja', 'codigo_sku'])['qtd_exp_calc_posicao'].transform('sum')

result_df.to_excel('Relatório_comercial_agrupado.xlsx', index=False)


result_df['qtd_exp_calc_total'] = result_df['qtd_exp_calc_total'].astype(float)
result_df['venda_30'] = result_df['venda_30'].astype(float)

remover_linhas = result_df['qtd_exp_calc_total'] <= result_df['venda_30']
result_df.loc[remover_linhas, 'análise'] = 'Remover'

# Drop rows where 'análise' is 'Remover'
result_df = result_df[result_df['análise'] != 'Remover']


# ------------ daqui pra cima

# Ajustando formatações
result_df['dt_inicio'] = pd.to_datetime(result_df['dt_inicio']).copy()
result_df['dt_fim'] = pd.to_datetime(result_df['dt_fim']).copy()
result_df['dt_log'] = pd.to_datetime(result_df['dt_log']).copy()

result_df['dt_inicio'] = result_df['dt_inicio'].dt.strftime('%d/%m/%Y').copy()
result_df['dt_fim'] = result_df['dt_fim'].dt.strftime('%d/%m/%Y').copy()
result_df['dt_log'] = result_df['dt_log'].dt.strftime('%d/%m/%Y').copy()

result_df['qtd_rep_cod_sku'] = result_df.groupby(['loja', 'codigo_sku'])['codigo_sku'].transform('count')
result_df['qtd_exp_calc_total'] = result_df['qtd_exp_calc_total'].round(0)
# result_df['qtd_exp_calc_total'] = result_df['qtd_exp_calc_total'].astype(int).astype(str)
result_df['qtd_exp_calc_total'] = result_df['qtd_exp_calc_total'].astype(int)


# Organizando as colunas
colunas_manter = ['comprador', 'exp_nome', 'loja', 'codigo_sku', 'nome_sku', 'posicao_movel',
                  'tipo_movel', 'venda_30', 'qtd_exp_calc_total', 'qtd_rep_cod_sku', 'análise']
result_df = result_df.loc[:, colunas_manter]

grupos_comprador = result_df.groupby('comprador')


if not result_df.empty:
    # Criar um arquivo Excel e adicionar abas para cada comprador
    arquivo_excel = "Relatório_comercial.xlsx"
    writer = pd.ExcelWriter(arquivo_excel, engine='openpyxl')

    # Adicionar cada grupo como uma aba separada
    for comprador, grupo in grupos_comprador:
        nome_aba = comprador[:31]  # Limitar o tamanho do nome da aba para 31 caracteres (limite do Excel)
        grupo.to_excel(writer, sheet_name=nome_aba, index=False)

    writer.close()
    print('Relatório_comercial gerado com Sucesso! ✅')
else:
    print('DataFrame vazio. Nenhum relatório foi gerado.🚨')

print('Relatório_comercial gerado com Sucesso!✅')