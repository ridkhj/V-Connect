from flask import Blueprint, jsonify, current_app
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json
from pathlib import Path

get_updates_bp = Blueprint('getupdates', __name__)

@get_updates_bp.route('/get-updates', methods=['GET'])
def get_updates():
    try:
        assets_path = Path(__file__).parent.parent.parent / 'assets'
        sheets_path = assets_path / 'sheets'
        file_path = sheets_path / 'atualizacoes.xlsx'

        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": "Arquivo não encontrado",
                "details": "Você precisa processar os arquivos primeiro",
                "errorType": "FILE_NOT_FOUND"
            }), 404

        sheetExtractor = SheetDataExtractor()
        updates = sheetExtractor.unity_process_sheet('atualizacoes.xlsx')
        
        if not updates:
            return jsonify({
                "success": False,
                "error": "Sem dados para processar",
                "details": "O arquivo existe mas está vazio ou não contém dados válidos",
                "errorType": "NO_DATA"
            }), 404

        data = object_to_json(updates)
        if isinstance(data, dict) and "error" in data:
            return jsonify({
                "success": False,
                "error": "Erro ao converter dados",
                "details": data["error"],
                "errorType": "CONVERSION_ERROR"
            }), 500

        return jsonify({
            "success": True,
            "data": data,
            "message": "Dados carregados com sucesso"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro interno: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e),
            "errorType": "SERVER_ERROR"
        }), 500

