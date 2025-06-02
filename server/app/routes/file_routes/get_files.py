from flask import Blueprint, jsonify, current_app
from pathlib import Path

get_files_bp = Blueprint('getfiles', __name__)

@get_files_bp.route('/get-csv-files', methods=['GET'])
def get_csv_files():
    """
    Lista todos os arquivos CSV disponíveis no diretório de assets
    ---
    responses:
      200:
        description: Arquivos CSV listados com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: exemplo.csv
                  path:
                    type: string
                    example: csv/exemplo.csv
                  size:
                    type: integer
                    example: 1024
                  modified:
                    type: number
                    format: float
                    example: 1717324832.0
            message:
              type: string
              example: Arquivos listados com sucesso
      404:
        description: Diretório não encontrado ou vazio
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: Nenhum arquivo encontrado
            details:
              type: string
              example: O diretório CSV está vazio
            errorType:
              type: string
              example: NO_FILES
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: Erro interno do servidor
            details:
              type: string
              example: Traceback detalhado do erro
            errorType:
              type: string
              example: SERVER_ERROR
    """
    try:
        assets_path = Path(__file__).parent.parent.parent / 'assets'
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
            files.append({
                "name": file.name,
                "path": str(file.relative_to(assets_path)),
                "size": file.stat().st_size,
                "modified": file.stat().st_mtime
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