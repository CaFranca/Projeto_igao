from flask import Flask
from controller.controller import blueprint_default as pagina
from model.model import MeuMiddleware

app = Flask(__name__)
app.secret_key = 'top_seguranca'  # Defina uma chave secreta para a sessão
app.register_blueprint(pagina)

# Registrar o middleware
app.wsgi_app = MeuMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
