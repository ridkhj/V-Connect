
from wsgiref import validate
from flask import Blueprint
from flask import request
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json


get_letters_pdf_bp = Blueprint('getletterspdf',__name__, url_prefix='/get-letters-pdf')

def get_letters(type):

    data = request.get_json()

    try:
        if not validate_type(type):
            return {"error" : "tipo inválido"}
    except ValueError as e:
        return {"error" : str(e)}

    if not data:
        return {"error": "Corpo da requisição vazio ou invpalido"}, 404  
    
    return data


get_letters_pdf_bp.get('/<type>')(get_letters)


def validate_type(type):
    valid_types = ['reciprocas', 'nsl', 'agradecimento']
    if type not in valid_types:
        raise ValueError(f"Tipo inválido: {type}. Tipos válidos: {', '.join(valid_types)}")
    return True



