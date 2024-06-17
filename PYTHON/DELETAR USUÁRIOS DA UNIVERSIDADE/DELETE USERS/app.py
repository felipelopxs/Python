import http.client

def delete_student(org_id, student_id, bearer_token):
    conn = http.client.HTTPSConnection("www.twygoead.com")
    url = f"/api/v1/o/{org_id}/students/{student_id}"
    payload = ''
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("DELETE", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(f"Deleted student ID {student_id}: {data.decode('utf-8')}")
    return student_id

# ID fixo da organização
org_id = "2461"

# Token de autorização Bearer
bearer_token = "9bdebd16d"

# Lê os IDs dos alunos do arquivo
with open(r"caminho", "r") as file:
    deleted_students = []
    for student_id in file:
        student_id = student_id.strip()  # Remove espaços em branco e quebras de linha
        deleted_students.append(delete_student(org_id, student_id, bearer_token))

# Salva os IDs dos alunos excluídos em um arquivo
with open(r"caminho", "w") as output_file:
    for student_id in deleted_students:
        output_file.write(f"{student_id}\n")
