from flask import Flask, Blueprint, render_template, request, abort,session,redirect, url_for

# Importar o modelo, se necessário
# from model.model import *

blueprint_default = Blueprint("blueprint_cool", __name__)

@blueprint_default.before_request
def request_info():
    print('Executa antes da requisição')

@blueprint_default.after_request
def responde_info(response):
    print('Executa antes da resposta')
    return response

@blueprint_default.route("/")
def index():
    if 'login' in session:
        return f'Bem-vindo, {session["login"]}'
    return render_template('erro.html')

@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['login']= request.form["login"]
        session['senha']= request.form["senha"]
        return redirect(url_for('index'))
    return render_template("index.html")

@blueprint_default.route('/home')
def home():
    return "Pagina inicial"

#@blueprint_default.route("/login", methods=["GET", "POST"])
#def login():
#    if request.method == "POST":
#        login = request.form.get("login")
#        senha = request.form.get("senha")
#        return render_template("index.html", login=login, senha=senha)
#    return render_template("index.html")



# Aplicar o decorator verificar_token à rota que precisa de autenticação
# @blueprint_default.route('/protected')
# @verificar_token
# def protected_route():
#     return "Esta é uma rota protegida!"
