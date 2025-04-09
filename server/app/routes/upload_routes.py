from flask import Blueprint, request, jsonify, current_app, render_template
from app.services.upload_service import handle_csv_upload

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method ==  'POST':
        if 'file' not in request.files:
            return jsonify({ "error": "No file part" }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({ "error": "No selected file" }), 400

        if file and file.filename.endswith('.csv'):
            result = handle_csv_upload(file, current_app.config['UPLOAD_FOLDER'])
            
            return jsonify({ "message": "File processed", "file": file.filename }), 200

        return jsonify({ "error": "Invalid file type" }), 400
    else:
        return render_template('upload.html')
