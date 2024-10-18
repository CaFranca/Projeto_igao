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
            return redirect(url_for('blueprint_cool.login')) 
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@blueprint_default.route("/")
def index():

    return redirect(url_for('blueprint_cool.login')) 

@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

  
        for usuario in usuarios:
            if usuario.login == login and usuario.senha == senha:
                session['login'] = login
                session['senha'] = senha
                
            
                if login == 'admin':
                    return redirect(url_for('blueprint_cool.admin_page'))
                
                return redirect(url_for('blueprint_cool.home')) 
       
        return render_template("erro.html")  

    return render_template("index.html")  

@blueprint_default.route('/home')
@login_required  
def home():
    return "Página inicial - Bem-vindo!"

@blueprint_default.route('/admin')
@login_required  
def admin_page():
    if session['login'] != 'admin':
        return redirect(url_for('blueprint_cool.index'))  
    return "Bem-vindo à página admin!"
