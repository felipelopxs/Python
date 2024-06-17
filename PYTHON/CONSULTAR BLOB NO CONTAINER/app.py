from azure.storage.blob import BlobServiceClient
from tqdm import tqdm

# Substitua os valores abaixo pelas suas credenciais do Azure
connection_string = "DefaultEndpointsProtocol=https;AccountName=**;AccountKey=***;EndpointSuffix=core.windows.net"


# Crie um cliente de serviço de blob
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Obtenha o container


# Nome do arquivo de texto contendo os nomes dos blobs
blob_names_file = r"caminho dos blobs"

# Nome do arquivo de texto para salvar os resultados
output_file = r"caminho que sera salvo o txt"

# Inicializar a barra de progresso com o número total de linhas no arquivo
total_lines = sum(1 for line in open(blob_names_file))
with tqdm(total=total_lines, desc="Verificando blobs") as pbar:
    # Abrir o arquivo de texto para escrever os resultados
    with open(output_file, 'w') as output:
        # Ler o arquivo de texto e verificar a existência dos blobs
        with open(blob_names_file, 'r') as file:
            for line in file:
                idcliente,blob_name = line.strip().split('|') # Remove espaços em branco e quebras de linha
                container_name = idcliente
                container_client = blob_service_client.get_container_client(container_name)
                try:
                    blob_client = container_client.get_blob_client(blob_name)
                    properties = blob_client.get_blob_properties()
                    output.write(f"O blob {blob_name} existe no container {container_name}.\n")
                except Exception as e:
                    output.write(f"O blob {blob_name} não existe no container {container_name}.\n")
                pbar.update(1)  # Atualiza a barra de progresso

print("Os resultados foram salvos no arquivo:", output_file)
