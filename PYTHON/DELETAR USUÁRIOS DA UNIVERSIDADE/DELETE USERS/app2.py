import http.client
from tqdm import tqdm

def delete_student(org_id, student_id, bearer_token):
    conn = http.client.HTTPSConnection("www.twygoead.com")
    url = f"/api/v1/o/{org_id}/students/{student_id}"
    payload = ''
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("DELETE", url, payload, headers)
    res = conn.getresponse()
    data = res.read().decode('utf-8')

    result = f"Deleted student ID {student_id}: {data}"
    return result

# ID fixo da organização
org_id = "2461"

# Token de autorização Bearer
bearer_token = "bd4956ef31d58f0c0b37f0ce81cb25060e72f34d53c9ab7ab3e59b3a3dc80500"

# Lê os IDs dos alunos do arquivo
with open(r"caminho", "r") as file:
    deleted_students_info = []
    
    # Adiciona tqdm para obter uma barra de progresso
    for student_id in tqdm(file, desc="Deleting students", unit="student"):
        student_id = student_id.strip()  # Remove espaços em branco e quebras de linha
        deleted_students_info.append(delete_student(org_id, student_id, bearer_token))

# Salva os resultados no arquivo "alunos_excluidos.txt"
output_file_path = r"caminho"
with open(output_file_path, "a") as output_file:
    for result in deleted_students_info:
        output_file.write(f"{result}\n")

print(f"Resultados salvos em: {output_file_path}")
