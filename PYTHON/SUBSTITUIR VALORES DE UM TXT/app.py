import re

# Lê o arquivo de entrada com a codificação 'utf-8'
with open(r'CAMINHO\rename.txt', 'r', encoding='utf-8') as arquivo_entrada:
    linhas = arquivo_entrada.readlines()

# Abre o arquivo de saída para escrita com a codificação 'utf-8'
with open(r'DCAMINHO\seuarquivo_modificado.txt', 'w', encoding='utf-8') as arquivo_saida:
    # Itera sobre cada linha no arquivo de entrada
    for linha in linhas:
        # Verifica se a linha já termina com uma extensão de arquivo válida
        if not re.search(r'\.\w+$', linha):
            # Divide a linha pelo caractere '|'
            partes = linha.split('|')

            # Pega a primeira parte e a extensão do arquivo
            primeira_parte = partes[0]
            extensao = primeira_parte[primeira_parte.rfind('.') + 1:]

            # Adiciona a extensão ao final da linha
            linha_modificada = linha.strip() + '.' + extensao + '\n'

            # Escreve a linha modificada no arquivo de saída
            arquivo_saida.write(linha_modificada)
        else:
            # Se a linha já tem uma extensão, escreve a linha original no arquivo de saída
            arquivo_saida.write(linha)

print("Concluído! Verifique o arquivo 'seuarquivo_modificado.txt'.")
