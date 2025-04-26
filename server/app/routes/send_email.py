from flask import Blueprint, request, jsonify
from flask_mail import Message

send_email_bp = Blueprint('send_email', __name__)

@send_email_bp.route('/send-email', methods=['POST'])
def enviar_email():
    data = request.get_json()   
    
    recipients = data.get('recipients')
    subject = data.get('subject')
    body = data.get('body')

    if not recipients or not subject or not body:
        return jsonify({'erro': 'Faltam campos obrigatórios'}), 400

    try:
        msg = Message(
            subject=subject,
            recipients=[recipients],
            body=body
        )

        from app import mail 
        mail.send(msg)
        
        return jsonify({'mensagem': 'E-mail enviado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
