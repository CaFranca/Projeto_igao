from flask import Blueprint, render_template, request, session, redirect, url_for, make_response,flash
from model.model import usuarios

blueprint_default = Blueprint("blueprint_cool", __name__)

# Area dos Cookies
@blueprint_default.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie has been set!")
    resp.set_cookie('username', 'Cazz', max_age=60*60*24)

@blueprint_default.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
     return f'The username is {username}'
    else:
        return 'No cookie found!'
    
@blueprint_default.route('/delete_cookie')
def delete_cookie():
    resp = make_response("Cookie has been deleted!")
    resp.set_cookie('username', '', expires=0)
    return resp
    
# Fim da area dos Cookies

# Area dos Request

##@blueprint_default.before_request
##def request_info():
##    print('Executa antes da requisição')
##
##@blueprint_default.after_request
##def responde_info(response):
##    print('Executa antes da resposta')
##    return response

def login_required(f):
    """Decorator para verificar se o usuário está logado."""
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('blueprint_cool.login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Fim da area dos Request

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
        
        # Redireciona para a página de erro com a mensagem
        flash('Credenciais incorretas', 'danger')
        return redirect(url_for('blueprint_cool.login'))  # Redireciona para o formulário de login

    return render_template("index.html")  # Exibe o login se o método não for POST


@blueprint_default.route('/home')
@login_required  # Garante que apenas usuários logados possam acessar
def home():
    return render_template("sucesso.html")

@blueprint_default.route('/admin')
@login_required  # Garante que apenas usuários logados possam acessar
def admin_page():
    if session['login'] != 'admin':
        return redirect(url_for('blueprint_cool.index'))  # Redireciona para login se não for admin
    flash('Formulario enviado com sucesso', 'success')
    return render_template("sucesso.html")



