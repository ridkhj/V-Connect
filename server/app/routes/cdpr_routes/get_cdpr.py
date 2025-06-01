from flask import Blueprint, jsonify, current_app
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json
from pathlib import Path

get_cdpr_bp = Blueprint('getcdpr',__name__)

@get_cdpr_bp.route('/get-cdpr', methods=['GET'])
def get_cdpr():
    try:
        assets_path = Path(__file__).parent.parent.parent / 'assets'
        sheets_path = assets_path / 'sheets'
        file_path = sheets_path / 'cdpr.xlsx'

        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": "Arquivo não encontrado",
                "details": "Você precisa processar os arquivos primeiro",
                "errorType": "FILE_NOT_FOUND"
            }), 404

        sheetExtractor = SheetDataExtractor()
        cdpr = sheetExtractor.unity_process_sheet('cdpr.xlsx')
        
        if not cdpr:
            return jsonify({
                "success": False,
                "error": "Sem dados para processar",
                "details": "O arquivo existe mas está vazio ou não contém dados válidos",
                "errorType": "NO_DATA"
            }), 404

        data = object_to_json(cdpr)
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
