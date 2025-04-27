from flask import request, send_file, Blueprint
from io import BytesIO
from app.services.generate_pdf_service import generate_pdf_service

generate_pdf_bp = Blueprint('generate_pdf', __name__) 

@generate_pdf_bp.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    dados = request.get_json()

    if not dados or 'pessoas' not in dados:
        return {"erro": "Dados inválidos"}, 400

    buffer = BytesIO()

    generate_pdf_service('RELÁTORIO DE PARTICIPANTES', dados, buffer)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='pessoas.pdf',
        mimetype='application/pdf'
    )
