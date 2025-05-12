from flask import request, send_file, Blueprint
from io import BytesIO
from app.scripts.csv_extractor import CsvExtractor


process_files_bp = Blueprint('processfiles',__name__)

@process_files_bp.route('/process-files', methods = ['POST'])

def process_files():

    dados = request.get_json()
    
    if not dados or '.csv' not in dados:
        return {"erro": "Dados inválidos"}, 400

    extrator = CsvExtractor()
    extrator.read_csv_in_pattern_folder()

    return jsonify({'mensagem': 'Arquivos processados com sucesso!'})
   

    