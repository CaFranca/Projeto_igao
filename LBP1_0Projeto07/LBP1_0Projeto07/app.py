from flask import Flask, render_template,flash
from controller.controller import blueprint_default as pagina
from model.model import MeuMiddleware

app = Flask(__name__)
app.secret_key = 'top_seguranca'  # Defina uma chave secreta para a sessão

# Configurações de segurança para cookies de sessão
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protege contra XSS
app.config['SESSION_COOKIE_SECURE'] = True  # Só envia o cookie via HTTPS


app.register_blueprint(pagina)

app.wsgi_app = MeuMiddleware(app.wsgi_app)


@app.errorhandler(404)
def page_not_found(e):
    flash('A url da pagina parece estar incorreta, tente voltar para a pagina de login','warning')
    return render_template('404.html'), 404

@app.errorhandler(403)
def acesso_negado(e):
    return render_template('403.html'), 403

@app.errorhandler(401)
def nao_autorizado(e):
    return render_template('401.html'), 401


# Manipulador de erros genéricos
@app.errorhandler(Exception)
def handle_generic_error(e):
    return render_template('erro.html', message=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
