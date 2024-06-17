import os
import shutil

def renomear_arquivos(pasta, arquivo_relacao, arquivo_erros):
    with open(arquivo_relacao, 'r', encoding='utf-8') as f:
        relacao = [linha.strip().split('|') for linha in f]

    correspondencia = {antigo: novo for antigo, novo in relacao}

    erros = []

    for arquivo_antigo, arquivo_novo in correspondencia.items():
        caminho_antigo = os.path.join(pasta, arquivo_antigo)
        caminho_novo = os.path.join(pasta, arquivo_novo)

        if os.path.exists(caminho_antigo):
            try:
                shutil.move(caminho_antigo, caminho_novo)
                print(f'Renomeado: {arquivo_antigo} para {arquivo_novo}')
            except Exception as e:
                print(f'Erro ao renomear {arquivo_antigo}: {e}')
                erros.append(arquivo_antigo)
        else:
            erros.append(arquivo_antigo)

    with open(arquivo_erros, 'w', encoding='utf-8') as f:
        f.write('\n'.join(erros))

if __name__ == "__main__":
    pasta = r"caminho"
    arquivo_relacao = r"caminho\rename.txt"
    arquivo_erros = "caminho\erros.txt"
    renomear_arquivos(pasta, arquivo_relacao, arquivo_erros)
