from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
 

MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=**;AccountKey=**;EndpointSuffix=core.windows.net"
MY_IMAGE_CONTAINER = "IDCONTAINER"
 
class AzureBlobImageProcessor:
  def __init__(self):
    print("Intializing AzureBlobImageProcessor")
 
    
    self.blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING).get_container_client(MY_IMAGE_CONTAINER)
 
  def change_content_type_for_jpg_files(self):
    print("changing content type for all files with .pdf extension")
 
    
    blob_list = self.blob_service_client.list_blobs()
    
    arquivos_alterados = 0
    
    for blob in blob_list:
      if ".pdf" in blob.name and "application/pdf" not in blob.content_settings["content_type"]:
 
        
        print(f"Alterando {blob.name}.")
 
        blob.content_settings.content_type = "application/pdf"
        self.blob_service_client.get_blob_client(blob).set_http_headers(blob.content_settings)
        
        arquivos_alterados += 1
        
        print(f"Alteração concluída.")
        
    print(f"{arquivos_alterados} arquivos alterados.")
 

azure_blob_image_processor = AzureBlobImageProcessor()
azure_blob_image_processor.change_content_type_for_jpg_files()