import http.client
from tqdm import tqdm

def inativar_aluno(org_id, student_id, bearer_token):
    conn = http.client.HTTPSConnection("universidade.arquivar.com")
    url = f"/api/v1/o/{org_id}/students/{student_id}/inactivate"
    payload = ''
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("DELETE", url, payload, headers)
    res = conn.getresponse()
    data = res.read().decode('utf-8')

    resultado = f"Aluno ID {student_id} inativado: {data}"
    return resultado

# ID fixo da organização
org_id = "2461"

# Token de autorização Bearer
bearer_token = "8555e386c520e***********"

# Lê os IDs dos alunos do arquivo
with open(r"caminho", "r") as arquivo:
    alunos_ids = [linha.strip() for linha in arquivo]
    
    alunos_inativados_info = []

    # Adiciona tqdm para obter uma barra de progresso
    for id_aluno in tqdm(alunos_ids, desc="Inativando alunos", unit=" alunos já inativados"):
        alunos_inativados_info.append(inativar_aluno(org_id, id_aluno, bearer_token))

# Salva os resultados no arquivo "alunos_inativados.txt"
caminho_saida = r"caminho"
with open(caminho_saida, "a") as arquivo_saida:
    for resultado in alunos_inativados_info:
        arquivo_saida.write(f"{resultado}\n")

print(f"Resultados salvos em: {caminho_saida}")
