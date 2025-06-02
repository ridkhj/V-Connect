from flask import Blueprint, jsonify, request, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
import os

upload_file_bp = Blueprint('uploadfile', __name__)

@upload_file_bp.route('/upload-file', methods=['POST'])
def upload_file():
    """
    Faz o upload de um ou mais arquivos CSV para o servidor.

    ---
    tags:
      - Arquivos
    summary: Upload de arquivos CSV
    description: >
      Permite o envio de um ou mais arquivos com extensão `.csv`. Os arquivos serão armazenados em um diretório interno da aplicação.
    consumes:
      - multipart/form-data
    parameters:
      - name: files
        in: formData
        type: file
        required: true
        description: Um ou mais arquivos CSV a serem enviados.
        collectionFormat: multi
    responses:
      200:
        description: Arquivos enviados com sucesso.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Arquivos enviados com sucesso
            data:
              type: object
              properties:
                files:
                  type: array
                  items:
                    type: string
                  example: ["exemplo1.csv", "exemplo2.csv"]
      400:
        description: Requisição inválida ou arquivos incorretos.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: Nenhum arquivo enviado
            details:
              type: string
              example: O campo 'files' é obrigatório
            errorType:
              type: string
              example: NO_FILE
      500:
        description: Erro interno no servidor ao processar o upload.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: Erro no upload de arquivo
            details:
              type: string
              example: Traceback do erro ou descrição detalhada
            errorType:
              type: string
              example: SERVER_ERROR
    """
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
