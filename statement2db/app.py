from flask.app import Flask
from flask_restful import Api

app = Flask(__name__, static_url_path='')
api = Api(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
