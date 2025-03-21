import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['MAX_CONTENT_LENGHT'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado', 400
        file = request.files ['file']

        if file.filename == '' or not file.filename.endswith('.csv'):
                return 'Arquivo inválido. Envie um arquivo .csv', 400
        # Salva o arquivo com um nome seguro
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Arquivo enviado com sucesso!'
    else:
        # Exibe o formulário para requisições GET
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

