import os
import shutil

def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def copy_and_rename(source, destination):
    with open(arquivo_txt, 'r',encoding='utf-8') as file, open(os.path.join(destination, 'nomes_finais.txt'), 'w',encoding='utf-8') as output_file:
        for line in file:
            try:
                old_name, new_name = line.strip().split('|')
                old_name = old_name.strip()
                new_name = new_name.strip()

                old_name = sanitize_filename(old_name)
                new_name = sanitize_filename(new_name)

                old_path = os.path.join(source, old_name)
                new_path = os.path.join(destination, new_name)

                if len(new_name) > 255:
                    new_name = old_name

                shutil.copy(old_path, new_path)
                output_file.write(f"{new_name}\n")
            
            except Exception as e:
                with open(os.path.join(destination, 'erros.txt'), 'a',encoding='utf-8') as error_file:
                    error_file.write(f"Erro ao processar linha '{line}': {str(e)}\n")

if __name__ == "__main__":
    source_path = r"caminho disco"
    arquivo_txt = r"***\rename.txt"
    destination_path = r"***\Arquivos"
    copy_and_rename(source_path, destination_path)
