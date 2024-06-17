from pdf2image import convert_from_path
import pytesseract as pt
import os
from PIL import Image
from tqdm import tqdm
import tempfile
from azure.storage.blob import BlobServiceClient
import fitz

Image.MAX_IMAGE_PIXELS = None

pt.pytesseract.tesseract_cmd = r'caminho'

# Defina a função get_text_from_any_pdf antes de usá-la
def get_text_from_any_pdf(pdf_file, start_page, end_page):
    images = convert_pdf_to_img(pdf_file, start_page, end_page)
    final_text = ""
    for pg, img in enumerate(images):
        final_text += convert_image_to_text(img)

    return final_text

def convert_pdf_to_img(pdf_file, start_page, end_page):
    return convert_from_path(pdf_file, 100, first_page=start_page, last_page=end_page, poppler_path=r"D:\poppler-23.11.0\Library\bin")

def convert_image_to_text(image_path):
    text = pt.image_to_string(image_path)
    return text

# Especifica o diretório onde serão salvos os arquivos
diretorio = r"caminho"

with open(diretorio + "\\Arquivos\\id.txt", "r") as arquivos:
    total_linhas = sum(1 for linha in arquivos)
    arquivos.seek(0)

    for linha in tqdm(arquivos, total=total_linhas, desc="PROGRESSO: "):
        try:
            
            idImagem = linha.strip()
            id = idImagem.strip('.')[0]
            caminho_download = os.path.join(diretorio, idImagem)
            path_to_pdf = f"{diretorio}\\{idImagem}"

            # Conectar ao serviço de blob do Azure
            connection_string = "DefaultEndpointsProtocol=https;AccountName=****************;AccountKey=******;EndpointSuffix=core.windows.net"
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            # Nome do contêiner e nome do blob
            container_name = "e4473541-f7fe-4ce6-a970-***********"
            blob_name = f"{idImagem.lower()}"

            # Fazer o download do blob
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            with open(caminho_download, "wb") as pasta:
                pasta.write(blob_client.download_blob().readall())
            
            documento = fitz.open(caminho_download)
            num_paginas = documento.page_count
            documento.close()

            # Processar o PDF em lotes de 10 páginas
            start_page = 0
            batch_size = 10
            total_pages = num_paginas  # Defina o total de páginas do seu PDF
            conteudo_paginas = ""
            while start_page < total_pages:
                end_page = min(start_page + batch_size, total_pages)
                conteudopdf = get_text_from_any_pdf(path_to_pdf, start_page + 1, end_page)
                #conteudopdf = conteudopdf.replace('\n', '').replace("'", "")
                conteudo_paginas += conteudopdf
                start_page += batch_size

            with open(f'{diretorio}\\insert.sql', 'a', encoding='utf8') as arquivoinsert:
                arquivoinsert.write("INSERT INTO tabela VALUES ('{}', '{}');\n".format(idImagem[:-4].upper(), conteudo_paginas.replace("\n", " ").replace("'", " ")))

                start_page += batch_size
            
            with open(diretorio + '\\LogSucesso.txt', 'a') as arquivosucesso:
                arquivosucesso.write(f"Sucesso: {idImagem} | IdImagem: {id} \n")

            os.remove(caminho_download) 
            
        except Exception as erro:
            erro = str(erro).replace('\n', ' ')
            with open(diretorio + '\\LogErro.txt', 'a') as arquivoerro:
                arquivoerro.write(f"Erro: {idImagem}|{erro}\n")
