
from flask import request, send_file, Blueprint, jsonify
from io import BytesIO
from app.services.generate_pdf import PdfGenerator
from app.utils.validators.update_validator import validate_update
from app.components.update import Update



    
get_updates_pdf_bp = Blueprint('getupdatespdf', __name__) 


@get_updates_pdf_bp.route('/get-updates-pdf', methods=['POST'])
def generate_updates_pdf():

    """
    Gera um arquivo PDF contendo dados de atualizações
    ---
    tags:
      - Atualizações
    summary: Gera um arquivo PDF a partir de dados de atualizações
    description: Recebe um payload JSON com dados de atualizações, valida os dados e retorna um arquivo PDF com os dados processados.
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
              - status
            properties:
              code:
                type: string
                description: O código da atualização
                example: "UPD123"
              name:
                type: string
                description: O nome associado à atualização
                example: "Atualização Sistema"
              status:
                type: string
                description: O status da atualização
                example: "Concluído"
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
                erro:
                  type: string
                  description: Mensagem de erro
              example:
                erro: "Validação falhou para os dados fornecidos."
      500:
        description: Erro interno do servidor
        content:
          application/json:
            schema:
              type: object
              properties:
                erro:
                  type: string
                  description: Mensagem de erro
              example:
                erro: "Erro interno do servidor"
    """
    dados = request.get_json()
    
    if not dados:
        return {"erro": "Nehum dado fornecido no corpo da reuiquisição"}, 400

    try:
        if not validate_update(dados):
            return jsonify({"erro": "Validação falhou para os dados fornecidos."}), 400
    except ValueError as e: 
        return jsonify({"erro", str(e)}), 400

    try: 
        updates = parse_updates(dados)
    except ValueError as e: 
        return jsonify({"erro" : str(e)}), 400

    
    pdf_generator = PdfGenerator()
    pdf_file = pdf_generator.create_updates_pdf(updates)

    return send_file(
        pdf_file,
        as_attachment=True,  
        download_name='atualizacoes.pdf',
        mimetype='application/pdf'
    )

def parse_updates(data):

    if isinstance(data, dict):
        data = [data]
    updates = []
    for item in data:
        code = item.get("code")
        name = item.get('name')
        status = item.get('status')

        if not all([code, name, status]):
            raise ValueError('Campos Obrigatórios [code, name, status] estão faltando em um ou mais objetos')

        update_obj = Update(code, name, status)
        updates.append(update_obj)  
    
    return updates

