from flask import Blueprint, jsonify, request, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
import os

upload_file_bp = Blueprint('uploadfile', __name__)

@upload_file_bp.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        if 'files' not in request.files:
            return jsonify({
                "success": False,
                "error": "Nenhum arquivo enviado",
                "details": "O campo 'files' é obrigatório",
                "errorType": "NO_FILE"
            }), 400

        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({
                "success": False,
                "error": "Nenhum arquivo selecionado",
                "details": "Por favor, selecione pelo menos um arquivo",
                "errorType": "NO_FILE_SELECTED"
            }), 400

        assets_path = Path(__file__).parent.parent / 'assets'
        csv_path = assets_path / 'csv'

        # Cria os diretórios se não existirem
        csv_path.mkdir(parents=True, exist_ok=True)

        uploaded_files = []
        for file in files:
            if file and file.filename.endswith('.csv'):
                filename = secure_filename(file.filename)
                file_path = csv_path / filename
                file.save(str(file_path))
                uploaded_files.append(filename)

        if not uploaded_files:
            return jsonify({
                "success": False,
                "error": "Nenhum arquivo CSV válido",
                "details": "Por favor, envie apenas arquivos CSV",
                "errorType": "INVALID_FILE_TYPE"
            }), 400

        return jsonify({
            "success": True,
            "message": "Arquivos enviados com sucesso",
            "data": {
                "files": uploaded_files
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro no upload de arquivo: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro no upload de arquivo",
            "details": str(e),
            "errorType": "SERVER_ERROR"
        }), 500
