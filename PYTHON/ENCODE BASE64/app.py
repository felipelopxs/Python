import base64
from reportlab.pdfgen import canvas

def base64_to_pdf(base64_data, output_filename='arquivo.pdf'):
    try:
        # Decodificar a string base64
        binary_data = base64.b64decode(base64_data)

        # Criar um arquivo PDF usando a biblioteca reportlab
        with open(output_filename, 'wb') as pdf_file:
            pdf_file.write(binary_data)

        print(f"Arquivo PDF criado com sucesso: {output_filename}")

    except Exception as e:
        print(f"Erro ao criar o arquivo PDF: {e}")

if __name__ == "__main__":
    
    base64_data = ''
    base64_to_pdf(base64_data)
