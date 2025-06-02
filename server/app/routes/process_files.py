from flask import jsonify, request, send_file, Blueprint
from app.scripts.csv_extractor import CsvExtractor


process_files_bp = Blueprint('processfiles',__name__)

@process_files_bp.route('/process-files', methods = ['POST'])

def process_files():

    """
    Processa arquivos CSV presentes em um diretório padrão.

    ---
    tags:
      - Arquivos
    summary: Processar arquivos CSV
    description: Lê e processa os arquivos CSV contidos em uma pasta padrão do projeto. Não requer parâmetros na requisição.
    responses:
      200:
        description: Arquivos processados com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Arquivos processados com sucesso!
      500:
        description: Erro interno ao processar os arquivos.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: Erro ao processar arquivos CSV
            details:
              type: string
              example: Traceback do erro ou descrição detalhada
    """
    #gerar verificação da pasta de arquivos
    
    extrator = CsvExtractor()
    extrator.read_csv_in_pattern_folder()

    return jsonify({'mensagem': 'Arquivos processados com sucesso!'})
   

    