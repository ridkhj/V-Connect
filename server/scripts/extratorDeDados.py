import openpyxl
from components.participante import Participante
from components.atualizacao import Atualizacao

def extrairDadosAtualizacao(path):
    arquivo = openpyxl.load_workbook(path)
    planilha = arquivo.active
    participantesPatos = []

    row = 2        # coordenadas da primeira celula a ser lida 
    column = 2
    acessar = planilha.cell

    while (acessar(row, column).value is not None and acessar(row, column+1).value is not None):

        codigo = acessar(row, column).value
        nome = acessar(row, column+1).value
        status = acessar(row, column+3).value

        
        participanteAuxiliar = Participante(codigo, nome, status)

        if status != "Enviado" and status != "Devolvido à Igreja Parceira":
    
            participantesPatos.append(participanteAuxiliar)
            
        row += 1

    return participantesPatos

def extrairDadosCDPR(path):
    arquivo = openpyxl.load_workbook(path)
    planilha = arquivo.active
    atualizacoes = []

    row = 2        # coordenadas da primeira celula a ser lida 
    column = 2
    acessar = planilha.cell

    while (acessar(row, column).value is not None and acessar(row, column+1).value is not None):

        codigo = acessar(row, column).value
        nome = acessar(row, column+1).value
        age = acessar(row, column+3).value

        
        atualizacoes.append(Atualizacao(codigo, nome, age))
 
        row += 1

    return atualizacoes
