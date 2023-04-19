import pandas as pd
import sqlite3
import numpy as np

# importar dados coletores
# importante, a primeira linha do txt tem que conter "Codigo;Coletor1" "Codigo;Coletor2" // criar scrip pra eliminar isso
coletor1 = pd.read_csv('coletor1.txt', sep=';')
coletor2 = pd.read_csv('coletor2.txt', sep=';')

# indicando qual será o index, no caso o código do produto coletado
coletor1.set_index('Codigo', inplace=True)
coletor2.set_index('Codigo', inplace=True)

# aqui fiz um agrupamento de ítens repetidos, por exemplo se no coletor 1 o produto foi contado em dois locais da empresa,
# então o sistema irá somar as contagens dos dois dentro da mesma coleta
coletor1agrupado = coletor1.groupby('Codigo').sum()
coletor2agrupado = coletor2.groupby('Codigo').sum()

# agrupar as planilhas e comparar itens para gerar relatorio de diferenca
planilha = coletor1agrupado.join(coletor2agrupado, how="outer")
planilha.fillna(0, inplace=True)
planilha['Diferença'] = planilha['Coletor1'] - planilha['Coletor2']
planilha['Diferença %'] = (planilha['Diferença'] / ((planilha['Coletor1'] + planilha['Coletor2'] / 2))) * 100

planilha.sort_index(inplace=True) #relatorio completo ordenado pelo codigo do produto

## relatórios de diferenças
planilha[planilha["Diferença"] == 0] # relatorio de produtos sem erro
planilha[planilha["Diferença"] != 0] # relatorio de produtos com erro
# opção 1 com margem de 1% de erro
diferenca_perc = planilha.query('`Diferença %` < -1 or `Diferença %` > 1')
# opção 2 com margem de 1% de erro
dif1 = planilha[planilha["Diferença %"] < -1]
dif2 = planilha[planilha["Diferença %"] > 1]
diferenca_perc = pd.concat([dif1, dif2])
diferenca_perc.sort_index(inplace=True)
