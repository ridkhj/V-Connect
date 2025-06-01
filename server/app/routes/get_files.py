from flask import Blueprint, jsonify, current_app
from pathlib import Path
from datetime import datetime
import uuid

get_files_bp = Blueprint('getfiles', __name__)

@get_files_bp.route('/get-csv-files', methods=['GET'])
def get_csv_files():
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