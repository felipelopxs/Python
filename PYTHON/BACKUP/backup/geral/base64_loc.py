# IMPORTANDO BIBLIOTECAS DE TERCEIROS
from base64 import b64decode



def decode(base64_string, caminho):

    decoded_bytes = b64decode(base64_string)
        
    # Salvando os bytes decodificados em um arquivo
    with open(caminho, "wb") as file:
        file.write(decoded_bytes)