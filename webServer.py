from flask import Flask
from flask.ext.login import LoginManager
from flask import Request
from flask import Response

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def login():


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)