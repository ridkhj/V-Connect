
from wsgiref import validate
from flask import Blueprint, send_file
from flask import request
from app.components.letter import Letter
from app.components.reciprocal_letter import ReciprocalLetter
from app.services.generate_pdf import PdfGenerator

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
    
    try:
        letters = parse_letters(type, data)
    except ValueError as e: 
        return {"error" :  str(e)}



    pdf_generator = PdfGenerator()
    pdf_file = pdf_generator.create_letters_pdf(letters)

    return send_file(
        pdf_file,
        as_attachment=True,  
        download_name='atualizacoes.pdf',
        mimetype='application/pdf'
    )


get_letters_pdf_bp.post('/<type>')(get_letters)


def validate_type(type):
    valid_types = ['reciprocas', 'nsl', 'agradecimento']
    if type not in valid_types:
        raise ValueError(f"Tipo inválido: {type}. Tipos válidos: {', '.join(valid_types)}")
    return True

def parse_letters(type, data):

    if isinstance(data, dict):
        data = [data]
    
    letters = []
   

    for item in data:

        code = item.get("code")
        letterCode = item.get("letterCode")
        name = item.get('name')
        letter_type = item.get('type')
        status = item.get('status')
        try:
            questions = item.get('questions')
        except ValueError:
            questions = None

        
        if not all([code, name, status, letterCode, letter_type]):
            raise ValueError('Campos Obrigatórios [code, name, status, letterCode, letter_type] estão faltando em um ou mais objetos')

        if questions is not None:
            letter_aux = ReciprocalLetter(code, letterCode, name, letter_type, status, None, questions)
        else:
            letter_aux = Letter(code, letterCode, name, letter_type, status)
        
        letters.append(letter_aux)

    return letters

