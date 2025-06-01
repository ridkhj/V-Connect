from flask import Blueprint, jsonify, current_app
from pathlib import Path

get_files_bp = Blueprint('getfiles', __name__)

@get_files_bp.route('/get-csv-files', methods=['GET'])
def get_csv_files():
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