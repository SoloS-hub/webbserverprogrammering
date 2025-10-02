from flask import Flask, request, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Sätter uppladdningsmappen i Flask-konfigurationen så den kan användas i hela appen och av tillägg
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # Kontrollerar om formuläret skickades med POST
        if 'the_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['the_file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # Rensar filnamnet för att förhindra katalogtraverseringsattacker
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Sparar filen i uppladdningsmappen
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))
        else:
            flash('File type not allowed')
            return redirect(request.url)
    # Denna mall visas för GET-requests och efter lyckad uppladdning
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
