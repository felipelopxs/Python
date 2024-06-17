import os
import shutil

def copiar_arquivos_por_extensao(origem, destino, extensao):
    # Verificar se o diretório de destino existe. Se não existir, criar.
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Percorrer todos os arquivos da pasta de origem
    for nome_arquivo in os.listdir(origem):
        # Verificar se o arquivo possui a extensão desejada
        if nome_arquivo.endswith(extensao):
            # Construir o caminho completo para o arquivo de origem
            caminho_origem = os.path.join(origem, nome_arquivo)
            # Construir o caminho completo para o arquivo de destino
            caminho_destino = os.path.join(destino, nome_arquivo)
            # Copiar o arquivo de origem para o destino
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"Arquivo {nome_arquivo} copiado com sucesso!")

# Exemplo de uso:
origem = r"I:\caminho"
destino = r"caminho\pdfs unificados"
extensao = ".pdf"

copiar_arquivos_por_extensao(origem, destino, extensao)
