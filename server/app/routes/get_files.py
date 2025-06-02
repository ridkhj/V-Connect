from flask import Blueprint, jsonify, current_app
from pathlib import Path
from datetime import datetime
import uuid

get_files_bp = Blueprint('getfiles', __name__)

@get_files_bp.route('/get-csv-files', methods=['GET'])
def get_csv_files():
    """
    Lista todos os arquivos CSV disponíveis no diretório de assets.

    ---
    tags:
      - Arquivos
    summary: Lista arquivos CSV
    description: Retorna uma lista de arquivos CSV encontrados no diretório `/assets/csv`, incluindo nome, tamanho, data de upload e um ID único.
    responses:
      200:
        description: Lista de arquivos retornada com sucesso.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Arquivos listados com sucesso
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                    example: "f9e1e2e4-bd72-4ef4-94e6-8b12d2de9a7d"
                  name:
                    type: string
                    example: "dados.csv"
                  size:
                    type: integer
                    example: 2048
                  uploadedAt:
                    type: string
                    format: date-time
                    example: "2024-06-01T12:34:56"
      404:
        description: Diretório não encontrado ou nenhum arquivo disponível.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Nenhum arquivo encontrado"
            details:
              type: string
              example: "O diretório CSV está vazio"
            errorType:
              type: string
              example: "NO_FILES"
      500:
        description: Erro interno do servidor.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Erro interno do servidor"
            details:
              type: string
              example: "Traceback do erro ou descrição"
            errorType:
              type: string
              example: "SERVER_ERROR"
    """

    try:
        assets_path = Path(__file__).parent.parent / 'assets'
        csv_path = assets_path / 'csv'

        if not csv_path.exists():
            return jsonify({
                "success": False,
                "error": "Diretório não encontrado",
                "details": "O diretório de arquivos CSV não existe",
                "errorType": "DIRECTORY_NOT_FOUND"
            }), 404

        files = []
        for file in csv_path.glob('*.csv'):
            stat = file.stat()
            files.append({
                "id": str(uuid.uuid4()),
                "name": file.name,
                "size": stat.st_size,
                "uploadedAt": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

        if not files:
            return jsonify({
                "success": False,
                "error": "Nenhum arquivo encontrado",
                "details": "O diretório CSV está vazio",
                "errorType": "NO_FILES"
            }), 404

        return jsonify({
            "success": True,
            "data": files,
            "message": "Arquivos listados com sucesso"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao listar arquivos: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e),
            "errorType": "SERVER_ERROR"
        }), 500 