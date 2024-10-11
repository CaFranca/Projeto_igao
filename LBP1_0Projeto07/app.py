from flask import Flask
from controller.controller import blueprint_default as pagina
from model.model import *

app = Flask(__name__)
app.register_blueprint(pagina)
app.wsgi_app=MeuMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
