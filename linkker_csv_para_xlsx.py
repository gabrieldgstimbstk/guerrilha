import pandas as pd 

dados0 = pd.read_csv('Planomax2.csv', sep=',')
dados1 = pd.read_csv('Planomax3.csv', sep=',')
dados2 = pd.read_csv('Planomax4.csv', sep=',')

dados = pd.concat(dados0,dados1,dados2)

dados.shape()
print('Li o Excel ✅')
print('-'*20)
dados.to_excel('linkker.xlsx',index=False)
print('Salvei Excel ✅')