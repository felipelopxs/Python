# IMPORTANDO BIBLIOTECAS INTERNAS
from logo import Logo



# IMPORTANDO BIBLIOTECAS DE TERCEIROS
import os
import shutil



def ValidadorDePasta(pasta):

    if os.path.isdir(pasta):
        pass
    else:
        os.makedirs(pasta)
        
def RemoverPasta(pasta):

    try:
        shutil.rmtree(pasta)
        
    except Exception as e:
        pass
        
def RemoverArquivo(arquivo):
    
    os.remove(arquivo)
    
def LimparTela():

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Logo())