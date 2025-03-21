from criarPdf import criar_pdf
import extratorDeDados as extratorDeDados
import extratorCSV as extratorCSV

extratorCSV.transformCsvToSheet()

participantesPatos = extratorDeDados.extrairDados(
    'V-Connect/client/src/scripts/assets/sheets/new.xlsx')

# if __name__ == "__main__":
criar_pdf("atualizaçõesPatos.pdf", participantesPatos)
# criar_pdf("atualizaçõesPrincesa.pdf", participantesPrincesa)