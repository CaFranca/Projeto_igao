from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, flash
from werkzeug.exceptions import HTTPException
import json  # Importa o módulo JSON
from model.model import usuarios
from functools import wraps

blueprint_default = Blueprint("blueprint_cool", __name__)

# Área dos Cookies
@blueprint_default.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie has been set!")
    resp.set_cookie('username', 'Cazz', max_age=60*24)
    return resp

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

# Função para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')  # Mensagem de aviso
            return redirect(url_for('blueprint_cool.login'))
        return f(*args, **kwargs)
    return wrapper

# Rota para tratar erro 404
@blueprint_default.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Manipulador de erros genéricos
@blueprint_default.errorhandler(Exception)
def handle_generic_error(e):
    return render_template('generic_error.html', message=str(e)), 500

# Página inicial
@blueprint_default.route("/")
def index():
    return redirect(url_for('blueprint_cool.login'))

# Rota de login
@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        # Verifica credenciais
        for usuario in usuarios:
            if usuario.login == login and usuario.senha == senha:
                session['login'] = login

                if login == 'admin':
                    return redirect(url_for('blueprint_cool.admin_page'))

                return redirect(url_for('blueprint_cool.home'))

        flash('Credenciais inválidas. Tente novamente.', 'danger')  # Mensagem de erro
        return redirect(url_for('blueprint_cool.login'))  # Redireciona para a página de login

    return render_template("index.html")

# Página protegida por login
@blueprint_default.route('/home')
@login_required
def home():
    return render_template("sucesso.html")

# Página do administrador
@blueprint_default.route('/admin')
@login_required
def admin_page():
    if session['login'] != 'admin':
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('blueprint_cool.index'))
    flash('A operação foi um sucesso', 'success')
    return render_template("sucesso.html")

# Logout
@blueprint_default.route('/logout')
@login_required
def logout():
    session.pop('login', None)  # Remove o usuário da sessão
    flash('Você foi desconectado com sucesso!', 'info')  # Mensagem de logout
    return redirect(url_for('blueprint_cool.login'))  # Redireciona para a página de login

# Página de produtos
@blueprint_default.route('/produtos')
@login_required
def produtos():
    produtos = [
        {'id': '1', 'nome': 'Produto A', 'preco': 10.00},
        {'id': '2', 'nome': 'Produto B', 'preco': 20.00},
        {'id': '3', 'nome': 'Produto C', 'preco': 30.00}
    ]
    return render_template("produtos.html", produtos=produtos)

# Adicionar ao carrinho
@blueprint_default.route('/adicionar_ao_carrinho', methods=["POST"])
@login_required
def adicionar_ao_carrinho():
    produto_id = request.form['produto_id']
    carrinho = request.cookies.get('carrinho')

    if carrinho:
        carrinho = json.loads(carrinho)  # Converte a string JSON de volta para um dicionário
    else:
        carrinho = {}

    if produto_id in carrinho:
        carrinho[produto_id] += 1  # Incrementa a quantidade
    else:
        carrinho[produto_id] = 1  # Adiciona o produto

    resp = make_response(redirect(url_for('blueprint_cool.produtos')))
    resp.set_cookie('carrinho', json.dumps(carrinho), max_age=60*60*24)  # Serializa o dicionário como JSON
    return resp

# Ver carrinho
@blueprint_default.route('/carrinho')
@login_required
def ver_carrinho():
    carrinho = request.cookies.get('carrinho')
    if carrinho:
        carrinho = json.loads(carrinho)  # Converte a string JSON de volta para um dicionário
    else:
        carrinho = {}

    return render_template("carrinho.html", carrinho=carrinho)
