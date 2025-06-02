from email import header
from os import name
from flask import request, send_file, Blueprint, jsonify
from io import BytesIO
from app.services.generate_pdf import PdfGenerator
from app.components.cdpr import Cdpr
from app.utils.validators.cdpr_validator import validate_cdpr
    
get_cdpr_pdf_bp = Blueprint('getcdprspdf', __name__) 


@get_cdpr_pdf_bp.route('/get-cdprs-pdf', methods=['POST'])
def generate_cdprs_pdf():

    """
    Gera um arquivo PDF contendo dados de CDPR
    ---
    tags:
      - CDPR
    summary: Gera um arquivo PDF a partir de dados de CDPR
    description: Recebe um payload JSON com dados de CDPR, valida os dados e retorna um arquivo PDF com os dados processados.
    consumes:
      - application/json
    produces:
      - application/pdf
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            required:
              - code
              - name
              - age
            properties:
              code:
                type: string
                description: O código do CDPR
                example: "CDPR123"
              name:
                type: string
                description: O nome associado ao CDPR
                example: "João Silva"
              age:
                type: integer
                description: A idade associada ao CDPR
                example: 30
    responses:
      200:
        description: Arquivo PDF gerado com sucesso
        content:
          application/pdf:
            schema:
              type: string
              format: binary
      400:
        description: Payload inválido ou validação falhou
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensagem de erro
              example:
                error: "Validação falhou para os dados fornecidos."
      500:
        description: Erro interno do servidor
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensagem de erro
              example:
                error: "Erro interno do servidor"
    """

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
    

