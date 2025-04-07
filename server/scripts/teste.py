import os
import pandas as pd
from extratorCSV import ExtratorCsv
import extratorDeDados as extratorDeDados
from criarPdf import criar_pdf_cdpr, criar_pdf_atualizacoes

def test_diferenciar_arquivos():

    csv_path = "D:/projetos/V-Connect/server/scripts/assets/csv/"

    arquivo_esperado = "D:/projetos/V-Connect/server/scripts/assets/sheets/atualizacoes.xlsx"
    arquivo_esperado2 = "D:/projetos/V-Connect/server/scripts/assets/sheets/cdpr.xlsx"
    if os.path.exists(arquivo_esperado):
        os.remove(arquivo_esperado)

    obj = ExtratorCsv(csv_path)
    obj.listarArquivos()

    assert os.path.exists(arquivo_esperado), "Arquivo não foi criado!" 
    assert os.path.exists(arquivo_esperado2), "Arquivo não foi criado!" 


def test_extrair_dados_atualizacoes():
    arquivo = "D:/projetos/V-Connect/server/scripts/assets/sheets/atualizacoes.xlsx"
    participantes = extratorDeDados.extrairDadosAtualizacao(arquivo)
    assert len(participantes) > 0, "Nenhum participante encontrado!"


    arquivo_esperado = "D:/projetos/V-Connect/server/scripts/atualizacoesPatos.pdf"
    if os.path.exists(arquivo_esperado):
        os.remove(arquivo_esperado)

    criar_pdf_atualizacoes("atualizacoesPatos.pdf", participantes, 'server/scripts/')

    assert os.path.exists(arquivo_esperado), "Arquivo não foi criado!" 


def test_extrair_dados_cdpr():
    arquivo = "D:/projetos/V-Connect/server/scripts/assets/sheets/cdpr.xlsx"
    atualizacoes = extratorDeDados.extrairDadosCDPR(arquivo)

    assert len(atualizacoes) > 0, "Nenhum dado encontrado!"


    arquivo_esperado2 = "D:/projetos/V-Connect/server/scripts/cdprPatos.pdf"
    if os.path.exists(arquivo_esperado2):
        os.remove(arquivo_esperado2)

    criar_pdf_cdpr("cdprPatos.pdf", atualizacoes, 'server/scripts/')

    assert os.path.exists(arquivo_esperado2), "Arquivo não foi criado!" 

    

if __name__ == "__main__":
    try:
        test_diferenciar_arquivos()
        print("✅ Teste CSV OK!")
    except AssertionError as e:
        print(f"❌ Teste CSV falhou: {e}")

    try:
        test_extrair_dados_atualizacoes()
        print("✅ Teste atualizacoes OK!")
    except AssertionError as e:
        print(f"❌ Teste atualizacoes falhou: {e}")

    try:
        test_extrair_dados_cdpr()
        print("✅ Teste CDPR OK!")
    except AssertionError as e:
        print(f"❌ Teste CDPR falhou: {e}")
