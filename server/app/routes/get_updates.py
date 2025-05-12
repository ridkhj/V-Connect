from flask import request, send_file, Blueprint
from io import BytesIO
from app.scripts.data_extractor import SheetDataExtractor
from json import dickter

get_updates_bp = Blueprint('getupdates',__name__)

@get_updates_bp.route('/get-updates', methods = ['GET'])

def get_updates():

    sheetExtractor = SheetDataExtractor()
    data = sheetExtractor.unity_process_sheet('atualizacoes.xlsx')
    if not data:
        return {"error": "Erro no processamento de arquivoss"}, 404
    