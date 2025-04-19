from flask import Blueprint, request, jsonify
from flask_mail import Message

send_email_bp = Blueprint('send_email', __name__)

@send_email_bp.route('/send-email', methods=['POST'])
def enviar_email():
    dados = request.get_json()
    
    destinatario = dados.get('destinatario')
    assunto = dados.get('assunto')
    corpo = dados.get('corpo')

    if not destinatario or not assunto or not corpo:
        return jsonify({'erro': 'Faltam campos obrigatórios'}), 400

    try:
        msg = Message(
            subject=assunto,
            recipients=[destinatario],
            body=corpo
        )

        from app import mail 
        mail.send(msg)
        
        return jsonify({'mensagem': 'E-mail enviado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
