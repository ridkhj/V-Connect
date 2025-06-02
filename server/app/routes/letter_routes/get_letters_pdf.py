
from wsgiref import validate
from flask import Blueprint, send_file
from flask import request
from app.components.letter import Letter
from app.components.reciprocal_letter import ReciprocalLetter
from app.services.generate_pdf import PdfGenerator

get_letters_pdf_bp = Blueprint('getletterspdf',__name__, url_prefix='/get-letters-pdf')

def get_letters(type):
    """
    Gera um arquivo PDF com cartas do tipo especificado
    ---
    tags:
      - Cartas
    summary: Gera um PDF contendo cartas com base no tipo fornecido
    description: Recebe um payload JSON com dados de cartas e um tipo de carta especificado no caminho da URL (reciprocas, nsl ou agradecimento). Valida os dados e gera um arquivo PDF com as cartas processadas. Suporta cartas normais (sem perguntas) e cartas recíprocas (com perguntas).
    consumes:
      - application/json
    produces:
      - application/pdf
    parameters:
      - name: type
        in: path
        required: true
        schema:
          type: string
          enum: ['reciprocas', 'nsl', 'agradecimento']
          example: 'reciprocas'
        description: Tipo de carta a ser gerada (reciprocas, nsl ou agradecimento)
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            required:
              - code
              - letterCode
              - name
              - type
              - status
            properties:
              code:
                type: string
                description: Código da carta
                example: "LTR123"
              letterCode:
                type: string
                description: Código específico da carta
                example: "LC456"
              name:
                type: string
                description: Nome associado à carta
                example: "João Silva"
              type:
                type: string
                description: Tipo da carta (deve corresponder ao parâmetro no caminho)
                example: "reciprocas"
              status:
                type: string
                description: Status da carta
                example: "Enviada"
              questions:
                type: array
                description: Lista de perguntas (obrigatória para cartas do tipo 'reciprocas', opcional para outros tipos)
                items:
                  type: string
                  example: "Qual é o status atual do projeto?"
    responses:
      200:
        description: Arquivo PDF gerado com sucesso
        content:
          application/pdf:
            schema:
              type: string
              format: binary
      400:
        description: Tipo inválido ou dados fornecidos inválidos
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensagem de erro
              example:
                error: "Tipo inválido: teste. Tipos válidos: reciprocas, nsl, agradecimento"
      404:
        description: Corpo da requisição vazio ou inválido
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensagem de erro
              example:
                error: "Corpo da requisição vazio ou inválido"
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

