import os
import traceback
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import landscape, A2
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# ler o arquivo Excel
df = pd.read_excel('CAMINHO\\historico_aditivo-aditivo_geral.xlsx')
#df = df.sort_values(by=['Data_Entrada'], ascending=[False])

# Obtendo os 'id_contrato' únicos
unique_ids = df['id_aditivo'].unique()

# Loop através dos 'id_contrato' únicos
for id in unique_ids:
    try:
        # Filtrar a planilha com o id_contrato atual
        filtered_df = df[df['id_aditivo'] == id]
        #filtered_df2 = df[df['Id_Aditivo'] == id]
        #filtered_df = filtered_df.sort_values(by=['Data_Entrada'], ascending=[False])
        
        # Criando arquivo de saída
        diretorio = f'pdf\\'
        os.makedirs(diretorio, exist_ok=True)

        pdf_file = os.path.join(diretorio,f'00_HISTORICO_DE_ETAPAS_{id}.pdf')
        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A2), leftMargin=1.27*cm, rightMargin=1.27*cm, topMargin=1.27*cm, bottomMargin=1.27*cm)
        
        elements = []
        
        # Criar tabela
        data = [filtered_df.columns.tolist()] + filtered_df.values.tolist()
        total_width = doc.width - doc.leftMargin - doc.rightMargin
        table = Table(data, repeatRows=1, colWidths=[None, None])
        
        # Configurar o estilo da tabela
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0),9),
            ('FONTSIZE', (0, 1), (0, -1), 9),
            ('LEADING', (0, 0), (-1, 0), 14),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, 0), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('SPLITBYROWSPAN', (0, 1), (-1, -1)),
        ]))
        
        header_data = ['HISTÓRICO DE ETAPAS']
        header_table = Table([header_data], repeatRows=1, colWidths=[doc.width], rowHeights=10)
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 18),
            ('LEADING', (0, 0), (-1, 0), 60),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE')
        ]))
        
        elements.append(header_table)
        elements.append(table)
        
        doc.build(elements)
        
        print(f'PDF gerado: {id}.')
        
    except Exception as e:
        print('Erro')
        
print('Processo finalizado!')