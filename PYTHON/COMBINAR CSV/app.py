import csv
import os

diretorio = "caminhodiretorio"
arquivo_saida = diretorio + "\\csvcombinados.csv"

arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv')]

with open(arquivo_saida, 'w', newline='', encoding='utf-8') as saida:
    escritor_csv = csv.writer(saida)

    for arquivo_csv in arquivos_csv:
        with open(os.path.join(diretorio, arquivo_csv), 'r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            for linha in leitor_csv:
                escritor_csv.writerow(linha)

print('Combinação concluída com sucesso!')
