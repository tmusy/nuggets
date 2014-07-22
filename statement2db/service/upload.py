import os

import flask
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        filename = do_the_upload(f)
        if filename:
            return "Upload successful"
        else:
            abort(400)
    else:
        abort(404)


def do_the_upload(upload_file):
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        upload_file.save(full_filename)
    return full_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
