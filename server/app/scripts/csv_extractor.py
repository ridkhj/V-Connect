from operator import contains
from numpy import printoptions
import pandas as pd
import os
from pathlib import Path


class CsvExtractor:
    
    def __init__(self):
        self._path = Path(__file__).parent.parent / 'assets' 
        
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def read_csv_in_pattern_folder(self):
        uploadedCsv= self.path / 'csv'
        if uploadedCsv.exists(): 
            arquivos = os.listdir(uploadedCsv)
            arquivos_csv = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
            print(arquivos_csv)
            for i in arquivos_csv:
               
                eachCsvPath = os.path.join(uploadedCsv, i)
             
                self.separate_csv_transform_to_sheet_by_type(eachCsvPath)
        else:
            raise FileNotFoundError(f"O diretório {uploadedCsv} não foi encontrado.")

    def separate_csv_transform_to_sheet_by_type(self, path):
        csv_path = path
        sheetsPath = self.path / 'sheets' 
        print(csv_path)
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
                 print("caiu em atualizações")
                 excelWriter = pd.ExcelWriter(sheetsPath / 'atualizacoes.xlsx')
                 break
            elif i == 'Idade e CDPR':
                 print("caiu em cdprs")
                 excelWriter = pd.ExcelWriter(sheetsPath / 'cdpr.xlsx')
                 break
            elif i == 'DBOP_03_B2SOVERDUEV4':
                 print("caiu em cartas relacionamento")
                 excelWriter = pd.ExcelWriter(sheetsPath / 'reciprocas.xlsx')
                 break
            elif i == 'DBOP_01_NSLV3':
                 print("caiu em cartas nsl")
                 excelWriter = pd.ExcelWriter(sheetsPath / 'nsl.xlsx')
                 break
            elif i == 'DBOP_12_THANKYOULETTERS':
                 print("caiu em cartas agradecimento")
                 excelWriter = pd.ExcelWriter(sheetsPath / 'agradecimento.xlsx')
                 break
            
        
            
        if excelWriter:
            csv.to_excel(excelWriter)
            excelWriter._save()
                