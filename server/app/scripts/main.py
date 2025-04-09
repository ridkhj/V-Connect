from criarPdf import criar_pdf_cdpr, criar_pdf_atualizacoes
from extratorDeDados import ExtratorDeDados
from extratorCSV import ExtratorCsv


extrator = ExtratorCsv(r'D:\projetos\V-Connect\server\scripts\assets\csv')
extrator.listarArquivos()


leitorDados = ExtratorDeDados('server/scripts/assets/sheets/')
leitorDados.listarArquivos()
#participantesPatos = leitorDados.extrairDadosAtualizacao('server/scripts/awssets/sheets/atualizacoes.xlsx')
#atualizacoes = leitorDados.extrairDadosCDPR('server/scripts/assets/sheets/cdpr.xlsx')

criar_pdf_cdpr("cdprPatos.pdf", leitorDados.cdprs, 'server/scripts/')
criar_pdf_atualizacoes("atualizacoesPatos.pdf", leitorDados.atualizacoes , 'server/scripts/')  