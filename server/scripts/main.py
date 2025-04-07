from criarPdf import criar_pdf_cdpr, criar_pdf_atualizacoes
import extratorDeDados as extratorDeDados
from extratorCSV import ExtratorCsv


extrator = ExtratorCsv('server/scripts/assets/csv')
extrator.listarArquivos()

participantesPatos = extratorDeDados.extrairDadosAtualizacao('server/scripts/assets/sheets/atualizacoes.xlsx')
atualizacoes = extratorDeDados.extrairDadosCDPR('server/scripts/assets/sheets/cdpr.xlsx')

criar_pdf_cdpr("cdprPatos.pdf", atualizacoes, 'server/scripts/')
criar_pdf_atualizacoes("atualizacoesPatos.pdf", participantesPatos, 'server/scripts/')  