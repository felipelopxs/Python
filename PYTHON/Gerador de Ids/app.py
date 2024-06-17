import uuid


num_ids = 88023 #Quantidade de ids que serão gerados
uuid_list = [uuid.uuid4() for _ in range(num_ids)]

# Nome do arquivo de texto
file_name = r"caminho"

# Salvando os UUIDs no arquivo de texto
with open(file_name, 'w') as file:
    for i, uuid_val in enumerate(uuid_list, start=1):
        file.write(f"{uuid_val}\n")

print(f"UUIDs foram salvos em {file_name}")
