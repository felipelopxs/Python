from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings

def update_blob_properties_and_metadata(blob_client, content_disposition, new_filename):
    # Obtenha as propriedades atuais
    blob_properties = blob_client.get_blob_properties()

    # Atualize as configurações de conteúdo
    content_settings = ContentSettings(
        content_disposition=content_disposition,
        content_type=blob_properties['content_settings']['content_type'],  # Mantenha o tipo de conteúdo original
    )

    # Atualize os metadados
    blob_properties['metadata']['filename'] = new_filename

    # Salve as alterações
    blob_data = blob_client.download_blob().readall()

    blob_client.upload_blob(data=blob_data , content_settings=content_settings, metadata=blob_properties['metadata'], overwrite=True)

def process_blob(blob_service_client, container_name, blob_info):
    container_client = blob_service_client.get_container_client(container_name)

    blob_name, content_disposition, new_filename = blob_info.strip().split('|')
    blob_client = container_client.get_blob_client(blob_name)

    # Faça suas alterações nas propriedades e metadados aqui
    update_blob_properties_and_metadata(blob_client, content_disposition, new_filename)

    print(f"Blob Name: {blob_name}")

def main():
    # Substitua pelos seus próprios valores
    connection_string = "DefaultEndpointsProtocol=https;AccountName=**;AccountKey=**;EndpointSuffix=core.windows.net"
    container_name = "INSIRA AQUI O ID DO CLIENTE"
    info_file_path = r"CAMINHO DO TXT DE IMGS"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Leia as informações do arquivo
    with open(info_file_path, 'r') as file:
        for line in file:
            process_blob(blob_service_client, container_name, line)

if __name__ == "__main__":
    main()
