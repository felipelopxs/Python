import os
import pandas as pd

# Carregue a planilha para um DataFrame do pandas
df = pd.read_excel(r'CAMINHO\Metadadis.xlsx')  # Substitua 'seu_arquivo.xlsx' pelo nome do seu arquivo Excel

# Especifique a coluna pela qual você deseja dividir as planilhas
coluna_divisao = 'Ano'  # Substitua 'sua_coluna' pelo nome da coluna

# Obtenha valores únicos na coluna de divisão
valores_unicos = df[coluna_divisao].unique()

# Especifique o caminho onde deseja salvar as planilhas
caminho_salvar = r'CAMINHO\Planilha'

# Crie planilhas separadas com base nos valores únicos
for valor in valores_unicos:
    planilha_individual = df[df[coluna_divisao] == valor]
    nome_planilha = f'Metadados_{valor}.xlsx'  # Nome da planilha com base no valor
    caminho_completo = os.path.join(caminho_salvar, nome_planilha)
    planilha_individual.to_excel(caminho_completo, index=False, header=True)  # Inclui o cabeçalho na planilha
