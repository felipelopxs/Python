def comparar_arquivos(arquivo1, arquivo2):
    with open(arquivo1, 'r', encoding='utf-8') as f1, open(arquivo2, 'r', encoding='utf-8') as f2:
        linhas1 = f1.readlines()
        linhas2 = f2.readlines()

        # Verifica se o número de linhas é o mesmo em ambos os arquivos
        if len(linhas1) != len(linhas2):
            print("Os arquivos têm diferentes números de linhas.")
            menor_numero_linhas = min(len(linhas1), len(linhas2))
        else:
            menor_numero_linhas = len(linhas1)

        # Compara os valores linha por linha
        for linha_num, (valor1, valor2) in enumerate(zip(linhas1, linhas2), start=1):
            valor1 = valor1.strip()
            valor2 = valor2.strip()

            if valor1 == valor2:
                print(f"Linha {linha_num}: Valores iguais - {valor1}")
            else:
                print(f"Linha {linha_num}: Valores diferentes - {valor1} (Arquivo 1) vs {valor2} (Arquivo 2)")

        # Se houver mais linhas em um dos arquivos, imprima as restantes
        for linha_num in range(menor_numero_linhas + 1, max(len(linhas1), len(linhas2)) + 1):
            if len(linhas1) > menor_numero_linhas:
                print(f"Linha {linha_num} (Arquivo 1): {linhas1[linha_num - 1].strip()}")
            if len(linhas2) > menor_numero_linhas:
                print(f"Linha {linha_num} (Arquivo 2): {linhas2[linha_num - 1].strip()}")

# Exemplo de uso
arquivo1 = 'planilha.txt'
arquivo2 = 'azure.txt'
comparar_arquivos(arquivo1, arquivo2)
