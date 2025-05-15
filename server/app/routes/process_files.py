from flask import jsonify, request, send_file, Blueprint
from app.scripts.csv_extractor import CsvExtractor


process_files_bp = Blueprint('processfiles',__name__)

@process_files_bp.route('/process-files', methods = ['POST'])

def process_files():

    #gerar verificação da pasta de arquivos
    
    extrator = CsvExtractor()
    extrator.read_csv_in_pattern_folder()

    return jsonify({'mensagem': 'Arquivos processados com sucesso!'})
   

    