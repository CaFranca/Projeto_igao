from flask import Flask
from controller.controller import blueprint_default as pagina
from model.model import MeuMiddleware

app = Flask(__name__)
app.secret_key = 'top_seguranca'
app.register_blueprint(pagina)
app.wsgi_app = MeuMiddleware(app.wsgi_app) 
# Registrar o middleware

if __name__ == "__main__":
    app.run(debug=True)
