import pandas as pd

# Funções

def ajustar_formato(valor):
    if isinstance(valor, str):
        valor = valor.replace('.', '').replace(',', '.')
    return valor      




# Guerrilha - ITENS MAPEADOS

# guerrilha_df = pd.read_csv('guerrilha.csv')
guerrilha_df = pd.read_excel('linkker.xlsx')

# Exposições - Cadastro de exposições
expositor_df = pd.read_csv('exp.csv', sep=';')

# Mix Total - Cadastro dos itens
mix_total_df = pd.read_csv('mix_total.csv', sep=';')


# Cadadatro de Usuário Abastecimento
# Informação do analista responsável no Abastecimento por departamento e seção
usuario_abasteciemento = pd.read_excel('cadastro_usuario_abastecimento.xlsx')

lojas_validas = [51, 108, 116, 124, 167, 175, 183, 205, 230, 248, 264, 272, 310, 329, 337]  # Loja sem regra de corte

posicoes_compativeis = ['PE', 'PG', 'ILHA'] # Pontos que são reconhecidos como válidos

lista_itens_em_linha = list(mix_total_df['RMS']) # lista dos itens em linha atualmente.

guerrilha_df['NÚMERO DA LOJA'] = guerrilha_df['NÚMERO DA LOJA'].astype(int)

colunas_manter = ['NÚMERO DA LOJA', 'TIPO DE PEX', 'NOME DO PONTO COMERCIALIZADO', 'SIGLA DO PONTO', 'Inicio', 'Fim',
                  'DATA DA VENDA', 'TIPO DE PERÍODO', 'USER QUE VENDEU', 'NOME SKU', 'CÓDIGO SKU']


guerrilha_df = guerrilha_df.loc[:, colunas_manter]

expositor_df['QTDVENDA_30_DIAS'] = pd.to_numeric(expositor_df['QTDVENDA_30_DIAS'].apply(ajustar_formato), errors='coerce')
