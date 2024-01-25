import pandas as pd 

dados = pd.read_csv('164d1f245ce5129889103ff66b025b03.csv', sep=',')
print('Li o Excel ✅')
print('-'*20)
dados.to_excel('linkker.xlsx',index=False)
print('Salvei Excel ✅')