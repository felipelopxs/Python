# IMPORTANDO BIBLIOTECAS DE TERCEIROS
import datetime

def DataHora() -> str:
    
    data_hora = datetime.datetime.now()
    data_hora = data_hora.strftime("%Y%m%d")
    
    return '20240306'
