import os
import threading
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_file_to_azure_blob(storage_connection_string, container_name, local_file_path, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Upload do arquivo {blob_name} concluído com sucesso.")
    except Exception as e:
        print(f"Erro ao fazer upload do arquivo {blob_name}: {str(e)}")

def upload_folder_to_azure_blob(storage_connection_string, container_name, local_folder_path, destination_folder):
    # Conectar-se ao serviço de armazenamento do Azure
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

    # Criar um container se ele não existir
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()

    # Percorrer todos os arquivos na pasta local
    for root, _, files in os.walk(local_folder_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            blob_name = os.path.join(destination_folder, os.path.relpath(local_file_path, local_folder_path).replace("\\", "/"))

            # Criar um thread para cada upload
            thread = threading.Thread(target=upload_file_to_azure_blob, args=(storage_connection_string, container_name, local_file_path, blob_name))
            thread.start()

if __name__ == "__main__":
    # Configurar as informações de conexão e parâmetros
    connection_string = "DefaultEndpointsProtocol=https;AccountName=arquivarstoragetmp;AccountKey=sJiLm6eSiIxO3l5dOn94F2I+UOdxhumzxaly7SA68LuyxjArp2aBg0HiVwWRWn4AkWzlIAyiUkXCJCU6kb1vOA==" 
    container_name = "328e6c72-d83b-4917-bf70-c5d44f965399bkp-final"
    local_folder_path = r"D:\CERVEJARIA - FINAL\WORKFLOW\Arquivos"
    destination_folder = "WORFKLOW/Arquivos/" # Replace with your desired folder name within the container

    # Fazer o upload da pasta e seus arquivos para o Blob do Azure
    upload_folder_to_azure_blob(connection_string, container_name, local_folder_path, destination_folder)
