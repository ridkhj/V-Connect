from flask import Blueprint
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json

get_updates_bp = Blueprint('getupdates',__name__)
 
@get_updates_bp.route('/get-updates', methods = ['GET'])

def get_updates():

    sheetExtractor = SheetDataExtractor()
    updates = sheetExtractor.unity_process_sheet('atualizacoes.xlsx')
    if not updates:
        return {"error": "Erro no processamento de arquivoss"}, 404
    
    json_data = object_to_json(updates)
    return json_data, 200




