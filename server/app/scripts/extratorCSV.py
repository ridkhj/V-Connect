import pandas as pd
import os
from pathlib import Path


class ExtratorCsv:
    
    def __init__(self):
        self._path = Path(__file__).parent.parent / 'assets' 
        
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def listarArquivos(self):
        uploadedCsv= self.path / 'csv'
        if uploadedCsv.exists(): 
            arquivos = os.listdir(uploadedCsv)
            arquivos_csv = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
            
            for i in arquivos_csv:
                print(uploadedCsv)
                print(f"Arquivo: {i}")
                eachCsvPath = os.path.join(uploadedCsv, i)
                print(f"Path: {eachCsvPath}")
                self.diferenciar_arquivos(eachCsvPath)
        else:
            raise FileNotFoundError(f"O diretório {uploadedCsv} não foi encontrado.")

    def diferenciar_arquivos(self, path):
        csv_path = path
        sheetsPath = self.path / 'sheets' 
        csv = pd.read_csv(csv_path, sep=";",
                          encoding="latin-1",
                          on_bad_lines="skip",
                          skipfooter=0 , engine="python",
                          quotechar='"',
                          na_values=[""],
                          )
        primeira_coluna = csv.iloc[:, 0]
        
        excelWriter = None
        for i in reversed(primeira_coluna):
            if i == "DBOP_08_UPDATES19OUMAIS":
                 excelWriter = pd.ExcelWriter(sheetsPath / 'atualizacoes.xlsx')
                 break
            elif i == "Idade e CDPR":
                 excelWriter = pd.ExcelWriter(sheetsPath / 'cdpr.xlsx')
                 break
            elif i == 'DBOP_03_B2SOVERDUEV4':
                 excelWriter = pd.ExcelWriter(sheetsPath / 'reciprocas.xlsx')
                 break
            elif i == 'DBOP_01_NSLV3':
                 excelWriter = pd.ExcelWriter(sheetsPath / 'nsl.xlsx')
                 break
            
        if excelWriter:
            csv.to_excel(excelWriter)
            excelWriter._save()
                