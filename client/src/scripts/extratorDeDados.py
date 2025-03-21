import openpyxl
from participante import Participante


def extrairDados(path):
    arquivo = openpyxl.load_workbook(path)
    planilha = arquivo.active
    participantesPatos = []

    row = 2        # coordenadas da primeira celula a ser lida 
    column = 2
    acessar = planilha.cell

    while (acessar(row, column).value != None):

        codigo = acessar(row, column).value
        nome = acessar(row, column+1).value
        status = acessar(row, column+3).value

        print(status)
        
        participanteAuxiliar = Participante(codigo, nome, status)

        if status != "Enviado" and status != "Devolvido à Igreja Parceira":
    
            participantesPatos.append(participanteAuxiliar)
            
        row += 1

    return participantesPatos
