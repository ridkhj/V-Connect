from os import name
from flask import request, send_file, Blueprint, jsonify
from io import BytesIO
from app.services.generate_pdf import PdfGenerator
from app.utils.validators.update_validator import validate_update
from app.components.update import Update



    
get_cdprs_pdf_bp = Blueprint('getcdprspdf', __name__) 


@get_cdprs_pdf_bp.route('/get-cdprs-pdf', methods=['POST'])
def generate_cdprs_pdf():

    data = request.get_json()

    if not data:
        return {"error":"Corpo vazio ou sem dados no corpo"}
    

    try:
        cdprs = parse_cdprs(data)
    except ValueError as e: 
        return jsonify({"error": str(e)})
    
    
    
    print(cdprs)
    return data


def parse_cdprs(data): 
    
    
    if isinstance(data, dict):
        data = [data]
    cdprs = [] 

    for item in data:
        name = item.get("code")
        code = item.get("code")
        age = item.get("age")

        if not all([code, name, age]):
            return ValueError('Campos Obrigatórios [code, name, status] estão faltando em um ou mais objetos')

        cdpr_aux = Update(code, name, age)
        cdprs.append(cdpr_aux)  

    return cdprs
    

