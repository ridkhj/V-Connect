
import pandas as pd

# esse arquivo, transforma um arquivo em csv para um arquivo "excel.xlsx"
# assim resolvando um problema de ter que fazer isso manualmente ao baixar
# as planilhas do connect, agora baixar diretamente no formato csv e está resolvido


def transformCsvToSheet():
    csv_path = "V-Connect/client/src/scripts/assets/csv/dados.csv"
    csv = pd.read_csv(csv_path, sep=";",
                      encoding="latin-1",
                      on_bad_lines="skip",
                      skipfooter=5, engine="python",
                      quotechar='"',
                      na_values=[""],
                      index_col=None,

                      )

    excelWriter = pd.ExcelWriter('V-Connect/client/src/scripts/assets/sheets/new.xlsx')
    csv.to_excel(excelWriter)
    excelWriter._save()
