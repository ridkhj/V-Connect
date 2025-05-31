from email import header
from os import name
from flask import request, send_file, Blueprint, jsonify
from io import BytesIO
from app.services.generate_pdf import PdfGenerator
from app.components.cdpr import Cdpr
from app.utils.validators.cdpr_validator import validate_cdpr
    
get_cdprs_pdf_bp = Blueprint('getcdprspdf', __name__) 


@get_cdprs_pdf_bp.route('/get-cdprs-pdf', methods=['POST'])
def generate_cdprs_pdf():

    data = request.get_json()

    if not data:
        return {"error":"Corpo vazio ou sem dados no corpo"}
    
    try: 
        if not validate_cdpr(data):
             return jsonify({"erro": "Validação falhou para os dados fornecidos."}), 400
    except ValueError as e: 
        return jsonify({"error": str(e)})
     
    try:
        cdprs = parse_cdprs(data)
    except ValueError as e: 
        return jsonify({"error": str(e)})
    
    pdf_generator = PdfGenerator()
    pdf_file = pdf_generator.create_cdpr_pdf(cdprs)
    
   
    return send_file(
        pdf_file,
        as_attachment= True,
        download_name='cdprs.pdf',
        mimetype='application/pdf'
    )


def parse_cdprs(data): 
    
    
    if isinstance(data, dict):
        data = [data]
    cdprs = [] 

    for item in data:
        
        code = item.get("code")
        name = item.get("name")
        age = item.get("age")

        if not all([code, name, age]):
            return ValueError('Campos Obrigatórios [code, name, status] estão faltando em um ou mais objetos')

        cdpr_aux = Cdpr(code, name, age)
        cdprs.append(cdpr_aux)  

    return cdprs
    

