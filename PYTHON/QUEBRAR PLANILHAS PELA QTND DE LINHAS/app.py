import pandas as pd
import openpyxl
import os

def quebrar_arquivo_excel(arquivo_entrada, linhas_por_arquivo, diretorio_destino):
    df = pd.read_excel(arquivo_entrada)

    total_linhas = df.shape[0]
    num_arquivos = (total_linhas // linhas_por_arquivo) + 1

    for i in range(num_arquivos):
        inicio = i * linhas_por_arquivo
        fim = (i + 1) * linhas_por_arquivo
        df_temp = df.iloc[inicio:fim]

        if df_temp.empty:
            break

        nome_arquivo_excel = os.path.join(diretorio_destino, f"arquivo_{i + 1}.xlsx")
        df_temp.to_excel(nome_arquivo_excel, index=False)

        nome_arquivo_csv = os.path.join(diretorio_destino, f"arquivo_{i + 1}.csv")
        workbook = openpyxl.load_workbook(nome_arquivo_excel)
        sheet = workbook.active
        data = sheet.values
        cols = next(data)
        df_temp = pd.DataFrame(data, columns=cols[1:])  # Ignorar o índice da coluna

        if len(df_temp.columns) != len(df.columns):
            raise ValueError(f"O número de colunas não coincide com o arquivo de entrada no arquivo {i + 1}")

        df_temp.to_csv(nome_arquivo_csv, index=False)

        # Fechar o arquivo Excel para liberar recursos
        workbook.close()

if __name__ == "__main__":
    arquivo_entrada = r"caminho\historico_contratos.xlsx"
    linhas_por_arquivo = 5000 #numnero de linhas
    diretorio_destino = r"caminho\QUEBRAR PLANILHAS PARA ARQIMPORT"  # Substitua pelo caminho desejado

    quebrar_arquivo_excel(arquivo_entrada, linhas_por_arquivo, diretorio_destino)
