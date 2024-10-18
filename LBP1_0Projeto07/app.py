from flask import Flask
from controller.controller import blueprint_default as pagina
from model.model import MeuMiddleware

app = Flask(__name__)
app.secret_key = 'top_seguranca'  # Defina uma chave secreta para a sessão

# Configurações de segurança para cookies de sessão
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protege contra XSS
app.config['SESSION_COOKIE_SECURE'] = True  # Só envia o cookie via HTTPS

# Registrar o Blueprint
app.register_blueprint(pagina)

# Registrar o middleware
app.wsgi_app = MeuMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
