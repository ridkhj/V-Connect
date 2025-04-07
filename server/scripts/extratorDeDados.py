import openpyxl
import os
from components.cdpr import Cdpr
from components.atualizacao import Atualizacao



class ExtratorDeDados:

    def __init__(self, path):
        self._path = path
        self._atualizacoes: list[Atualizacao] = []
        self._cdprs: list[Cdpr] = []
        
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def atualizacoes(self):
        return self._atualizacoes

    @atualizacoes.setter
    def atualizacoes(self, value: list[Atualizacao]):
        self._atualizacoes = value

    @property
    def cdprs(self):
        return self._cdprs

    @cdprs.setter
    def cdprs(self, value: list[Cdpr]):
        self._cdprs = value

    def listarArquivos(self):
        arquivos = os.listdir(self.path)
        arquivos_xlsx = [arquivo for arquivo in arquivos if arquivo.endswith('.xlsx')]
        for arquivo in arquivos_xlsx:
            if arquivo.startswith('atualizacoes'):
                self.extrairDadosAtualizacao(os.path.join(self.path, arquivo))
            elif arquivo.startswith('cdpr'): 
                self.extrairDadosCDPR(os.path.join(self.path, arquivo))   
                
    def extrairDadosAtualizacao(self, path):
        arquivo = openpyxl.load_workbook(path)
        planilha = arquivo.active
        atualizacoes = []

        row = 2        # coordenadas da primeira celula a ser lida 
        column = 2
        acessar = planilha.cell

        while (acessar(row, column).value is not None and acessar(row, column+1).value is not None):

            codigo = acessar(row, column).value
            nome = acessar(row, column+1).value
            status = acessar(row, column+3).value

            
            atualizacaoAux = Atualizacao(codigo, nome, status)

            if status != "Enviado" and status != "Devolvido à Igreja Parceira":
        
                atualizacoes.append(atualizacaoAux)
                
            row += 1

        self.atualizacoes = atualizacoes

    def extrairDadosCDPR(self, path):
        arquivo = openpyxl.load_workbook(path)
        planilha = arquivo.active
        cdprs = []

        row = 2        # coordenadas da primeira celula a ser lida 
        column = 2
        acessar = planilha.cell

        while (acessar(row, column).value is not None and acessar(row, column+1).value is not None):

            codigo = acessar(row, column).value
            nome = acessar(row, column+1).value
            age = acessar(row, column+3).value

            cdprs.append(Cdpr(codigo, nome, age))
    
            row += 1

        self.cdprs = cdprs