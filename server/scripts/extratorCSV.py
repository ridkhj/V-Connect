import pandas as pd
import os


class ExtratorCsv:
    
    def __init__(self, path):
        self._path = path
        
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def listarArquivos(self):
        arquivos = os.listdir(self._path)
        arquivos_csv = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
        
        for i in arquivos_csv:
            print(self.path)
            print(f"Arquivo: {i}")
            csvPath = os.path.join(self.path, i)
            print(f"Path: {csvPath}")
            self.diferenciar_arquivos(csvPath)

    def diferenciar_arquivos(self, path):
        csv_path = path
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
                 excelWriter = pd.ExcelWriter('server/scripts/assets/sheets/atualizacoes.xlsx')
                 break
            elif i == "Idade e CDPR":
                 excelWriter = pd.ExcelWriter('server/scripts/assets/sheets/cdpr.xlsx')
                 break
            
        if excelWriter:
            csv.to_excel(excelWriter)
            excelWriter._save()
                