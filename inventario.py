import pandas as pd
import sqlite3
import numpy as np

# importar dados coletores
# importante, a primeira linha do txt tem que conter "Codigo;Coletor1" "Codigo;Coletor2" // criar scrip pra eliminar isso
coletor1 = pd.read_csv('coletor1.txt', sep=';')
coletor2 = pd.read_csv('coletor2.txt', sep=';')

coletor1.set_index('Codigo', inplace=True)
coletor2.set_index('Codigo', inplace=True)
coletor1agrupado = coletor1.groupby('Codigo').sum()
coletor2agrupado = coletor2.groupby('Codigo').sum()

# comparar itens e gerar relatorio de diferenca, pode usar qualquer uma das opções à seguir
#planilha = pd.merge(coletor1agrupado, coletor2agrupado, how="outer", on='Codigo')
planilha = coletor1agrupado.join(coletor2agrupado, how="outer")
planilha.fillna(0, inplace=True)
planilha['Diferença'] = planilha['Coletor1'] - planilha['Coletor2']
planilha['Diferença %'] = (planilha['Diferença'] / ((planilha['Coletor1'] + planilha['Coletor2'] / 2))) * 100
planilha.sort_index(inplace=True)

# relatórios de diferenças
planilha[planilha["Diferença"] == 0]
planilha[planilha["Diferença"] != 0]
# opção 1 com margem de 1%
diferenca_perc = planilha.query('`Diferença %` < -1 or `Diferença %` > 1')
# opção 2 com margem de 1%
dif1 = planilha[planilha["Diferença %"] < -1]
dif2 = planilha[planilha["Diferença %"] > 1]
diferenca_perc = pd.concat([dif1, dif2])
diferenca_perc.sort_index(inplace=True)

# concatenar as duas planilha[planilha["Diferença %"] <= -1] [planilha["Diferença %"] >= 1]

# ordenar itens
# coletor1.sort_index()
# coletor2.sort_index()
# apagar coluna
# del planilha["Diferença"]
# selecionar somente uma coluna, identificar o dataframe e a coluna assim:
# coletor1['item']
