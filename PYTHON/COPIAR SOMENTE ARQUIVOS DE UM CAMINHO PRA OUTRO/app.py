import os
import shutil

def copiar_arquivos(diretorio_origem, diretorio_destino):
    for raiz, subpastas, arquivos_na_pasta in os.walk(diretorio_origem):
        for arquivo in arquivos_na_pasta:
            caminho_arquivo_origem = os.path.join(raiz, arquivo)
            caminho_arquivo_destino = os.path.join(diretorio_destino, arquivo)
            shutil.copy2(caminho_arquivo_origem, caminho_arquivo_destino)

# Exemplo de uso
diretorio_origem = r'caminho origem'  
diretorio_destino = r'caminho destino'  

copiar_arquivos(diretorio_origem, diretorio_destino)
