from criarPdf import PdfGenerator
from extratorDeDados import ExtratorDeDados
from extratorCSV import ExtratorCsv


extrator = ExtratorCsv()
extrator.listarArquivos()


leitorDados = ExtratorDeDados()
leitorDados.listarArquivos()


#participantesPatos = leitorDados.extrairDadosAtualizacao('server/scripts/awssets/sheets/atualizacoes.xlsx')
#atualizacoes = leitorDados.extrairDadosCDPR('server/scripts/assets/sheets/cdpr.xlsx')
geradorPdf = PdfGenerator()


geradorPdf.criar_pdf_atualizacoes("atualizacoesPatos.pdf", leitorDados.atualizacoes )  
geradorPdf.criar_pdf_cdpr("cdprPatos.pdf", leitorDados.cdprs)