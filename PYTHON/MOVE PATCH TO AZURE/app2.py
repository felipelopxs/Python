import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_folder_to_azure_blob(storage_connection_string, container_name, local_folder_path, destination_folder):
    # Conectar-se ao serviço de armazenamento do Azure
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

    # Criar um container se ele não existir
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()

    # Listas para rastrear arquivos com erro e sucesso
    arquivos_com_erro = []
    arquivos_com_sucesso = []

    # Inicializar contador de documentos enviados
    documentos_enviados = 0

    # Percorrer todos os arquivos na pasta local
    for root, _, files in os.walk(local_folder_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            blob_name = os.path.join(destination_folder, os.path.relpath(local_file_path, local_folder_path).replace("\\", "/"))

            # Criar um BlobClient para o arquivo
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            try:
                # Fazer upload do arquivo para o blob
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data)
                arquivos_com_sucesso.append(blob_name)
                documentos_enviados += 1

                # Imprimir o progresso
                print(f"Enviando documento {documentos_enviados}/{len(files)}: {blob_name}")
            except Exception as e:
                print(f"Erro ao fazer upload do arquivo {blob_name}: {str(e)}")
                arquivos_com_erro.append(blob_name)

    # Criar arquivo TXT com arquivos com erro
    with open(r"caminho\arquivos_com_erro.txt", "w") as erro_file:
        for arquivo_erro in arquivos_com_erro:
            erro_file.write(f"{arquivo_erro}\n")

    # Criar arquivo TXT com arquivos com sucesso
    with open(r"caminho\arquivos_com_sucesso.txt", "w") as sucesso_file:
        for arquivo_sucesso in arquivos_com_sucesso:
            sucesso_file.write(f"{arquivo_sucesso}\n")

    print(f"Envio concluído. {documentos_enviados} documentos enviados com sucesso.")

if __name__ == "__main__":
    # Configurar as informações de conexão e parâmetros
    connection_string = "DefaultEndpointsProtocol=https;AccountName=***storagetmp;AccountKey=*********" 
    container_name = "328e6c72-d83b-4917-bf70-c5d44f965399bkp-final"
    local_folder_path = r"caminho\Arquivos"
    destination_folder = "WORFKLOW/Arquivos/" # Replace with your desired folder name within the container

    # Fazer o upload da pasta e seus arquivos para o Blob do Azure
    upload_folder_to_azure_blob(connection_string, container_name, local_folder_path, destination_folder)
