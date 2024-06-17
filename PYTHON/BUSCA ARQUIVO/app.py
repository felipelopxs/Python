import os

def buscar_arquivo(nome_arquivo, diretorio):
    caminho_arquivo = None
    for root, dirs, files in os.walk(diretorio):
        if nome_arquivo in files:
            caminho_arquivo = os.path.join(root, nome_arquivo)
            break
    return caminho_arquivo

def main():
    nome_arquivo = input("Digite o nome do arquivo que deseja procurar: ")
    discos = [f"{chr(i)}:\\" for i in range(65, 91)]  # Lista de letras de unidades de disco (A:, B:, ..., Z:)
    
    print(discos)
    discos = ["C:\\"]
    print(discos)
    
    for disco in discos:
        if os.path.exists(disco):
            caminho_arquivo = buscar_arquivo(nome_arquivo, disco)
            if caminho_arquivo:
                print(f'O arquivo {nome_arquivo} foi encontrado em: {caminho_arquivo}')
                break
    else:
        print(f'O arquivo {nome_arquivo} não foi encontrado em nenhum disco.')

if __name__ == "__main__":
    main()
