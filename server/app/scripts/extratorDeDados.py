import openpyxl
import os
from components.cdpr import Cdpr
from components.atualizacao import Atualizacao
from components.carta import Carta
from pathlib import Path 



class ExtratorDeDados:

    def __init__(self):
        self._path = Path(__file__).parent.parent / 'assets'
        self._atualizacoes: list[Atualizacao] = []
        self._cdprs: list[Cdpr] = []
        self._cartas: list[Carta] = []
        
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
        loadPath = self.path / 'sheets'
        if loadPath.exists():
            arquivos = os.listdir(loadPath)
            arquivos_xlsx = [arquivo for arquivo in arquivos if arquivo.endswith('.xlsx')]
            for arquivo in arquivos_xlsx:
                if arquivo.startswith('atualizacoes'):
                    self.extrairDadosAtualizacao(os.path.join(loadPath, arquivo))
                elif arquivo.startswith('cdpr'): 
                    self.extrairDadosCDPR(os.path.join(loadPath, arquivo)) 
                elif arquivo.startswith('reciprocas'):
                    self.extrairDadosReciprocas(os.path.join(loadPath, arquivo))
        else:
            raise FileNotFoundError(f"O diretório {loadPath} não foi encontrado.")
                
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
    
    def extrairDadosReciprocas(self, path):
        arquivo = openpyxl.load_workbook(path)
        planilha = arquivo.active
        cartas = []

        row = 2        # coordenadas da primeira celula a ser lida 
        column = 2
        acessar = planilha.cell

        while (acessar(row, column).value is not None and acessar(row, column+1).value is not None):

            code = acessar(row, column).value
            letterCode = acessar(row, column+1).value
            name = acessar(row, column+3).value
            type = acessar(row, column+6).value
            questions = acessar(row, column+7).value
            status = acessar(row, column+13).value   
            print(code, letterCode, name, type, status)
            cartas.append(Carta(code, letterCode, name, type, questions, status))
            row += 1

        self._cartas = cartas