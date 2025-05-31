from flask import Blueprint 
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json

get_cdpr_bp = Blueprint('getcdpr',__name__)

@get_cdpr_bp.route('/get-cdpr', methods = ['GET'])
def get_cdpr():
    
    sheetExtractor = SheetDataExtractor()
    cdpr = sheetExtractor.unity_process_sheet('cdpr.xlsx')
    if not cdpr:
        return {"error": "Erro no processamento de arquivos"}, 404
    
    json_data = object_to_json(cdpr)
    return json_data, 200