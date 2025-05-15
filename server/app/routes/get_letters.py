from flask import Blueprint
from flask import request
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json


get_letters_bp = Blueprint('getletters',__name__, url_prefix='/get-letters')

def get_letters():

    data = request.get_json()
    type = data.get('type')
    
    sheetExtractor = SheetDataExtractor()
    letters = sheetExtractor.unity_process_sheet(type)
    
    if not letters:
        return {"error": "Erro no processamento de arquivos"}, 404  
    letters_json = object_to_json(letters)
    return letters_json, 200

get_letters_bp.get('/<type>')(get_letters())



