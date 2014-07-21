import os

import flask
from werkzeug.utils import secure_filename

from statement2db.lib.parser import parse


UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        return do_the_upload(file)
    else:
        return show_the_upload_form()

def do_the_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_filename)
        content = parse(full_filename)
        #return redirect(url_for('uploaded_file', filename=filename))
    return flask.render_template('document.html', content=content)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def show_the_upload_form():
    return flask.render_template('upload.html')

if __name__ == '__main__':
    app.run()
