from flask import Blueprint, render_template, request, session, redirect, url_for
from model.model import usuarios

blueprint_default = Blueprint("blueprint_cool", __name__)

@blueprint_default.before_request
def request_info():
    print('Executa antes da requisição')

@blueprint_default.after_request
def responde_info(response):
    print('Executa antes da resposta')
    return response

def login_required(f):
    """Decorator para verificar se o usuário está logado."""
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('blueprint_cool.login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@blueprint_default.route("/")
def index():
    # Redireciona para a página de login
    return redirect(url_for('blueprint_cool.login')) 

@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        # Verifica se o usuário e a senha estão corretos
        for usuario in usuarios:
            if usuario.login == login and usuario.senha == senha:
                session['login'] = login
                session['senha'] = senha
                
                # Redireciona para /admin se o usuário for admin
                if login == 'admin':
                    return redirect(url_for('blueprint_cool.admin_page'))
                
                return redirect(url_for('blueprint_cool.home'))  # Ou para a página inicial
       
        return render_template("erro.html")  # Renderiza a página de erro se as credenciais estiverem incorretas

    return render_template("index.html")  # Exibe o login se o método não for POST

@blueprint_default.route('/home')
@login_required  # Garante que apenas usuários logados possam acessar
def home():
    return "Página inicial - Bem-vindo!"

@blueprint_default.route('/admin')
@login_required  # Garante que apenas usuários logados possam acessar
def admin_page():
    if session['login'] != 'admin':
        return redirect(url_for('blueprint_cool.index'))  # Redireciona para login se não for admin
    return "Bem-vindo à página admin!"
