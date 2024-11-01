from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, flash,abort
from model.model import usuarios
import json; from functools import wraps;  from collections import defaultdict
blueprint_default = Blueprint("blueprint_cool", __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            abort(403)
            #return redirect(url_for('blueprint_cool.login'))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('login') != 'admin':
            flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
            abort(401)
            #return redirect(url_for('blueprint_cool.index'))
        return f(*args, **kwargs)
    return wrapper

@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        usuario_encontrado = False  # Variável para verificar se o usuário existe

        for usuario in usuarios:
            if usuario.login == login:  # Se o login do usuário for encontrado
                usuario_encontrado = True  # Usuário existe
                
                if usuario.senha == senha:  # Verifica se a senha está correta
                    session['login'] = login  # Armazena o login na sessão
                    
                    # Redireciona conforme o tipo de usuário
                    if login == 'admin':
                        return redirect(url_for('blueprint_cool.admin_page'))
                    return redirect(url_for('blueprint_cool.home'))

                # Se a senha estiver incorreta
                flash('Senha incorreta. Tente novamente.', 'danger')
                return redirect(url_for('blueprint_cool.login'))

        # Se o usuário não foi encontrado
        if not usuario_encontrado:
            flash('Credenciais de usuários inválidas. Tente novamente.', 'danger')
            return redirect(url_for('blueprint_cool.login'))

    # Para GET
    return render_template("index.html")


# Página inicial
@blueprint_default.route("/")
def index():
    return redirect(url_for('blueprint_cool.login'))

# Página protegida por login
@blueprint_default.route('/home')
@login_required
def home():
    return render_template("sucesso.html")

# Página do administrador
@blueprint_default.route('/admin')
@login_required
@admin_required  # Adicionando a verificação de administrador
def admin_page():
    flash('A operação foi um sucesso', 'success')
    return render_template("sucesso.html")


# Logout
@blueprint_default.route('/logout')
@login_required
def logout():
    session.pop('login', None)
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('blueprint_cool.login'))

# Página de produtos
@blueprint_default.route('/produtos')
@login_required
def produtos():
    produtos = [
        {'id': '1', 'nome': 'NVIDIA GeForce RTX 3060', 'preco': 2499.90, 'image':'images/rtx3060.jpg'},
        {'id': '2', 'nome': 'AMD Radeon RX 6700 XT', 'preco': 2999.99, 'image':'images/AMD Radeon RX 6700 XT.jfif'},
        {'id': '4', 'nome': 'NVIDIA GeForce RTX 3090', 'preco': 2999.99, 'image':'images/NVIDIA GeForce RTX 3090.jfif'},
        {'id': '3', 'nome': 'NVIDIA GeForce GTX 1660 Super', 'preco': 1799.90, 'image':'images/NVIDIA GeForce GTX 1660 Super.jfif'}
    ]

    return render_template("produtos.html", produtos=produtos)

# Adicionar ao carrinho
@blueprint_default.route('/adicionar_ao_carrinho', methods=["POST"])
@login_required
def adicionar_ao_carrinho():
    produto_id = request.form['produto_id']
    
    # Recupera o carrinho do cookie e converte de volta para dicionário
    carrinho = json.loads(request.cookies.get('carrinho', '{}'))
    
    # Usa defaultdict para evitar verificações manuais de existência
    carrinho = defaultdict(int, carrinho)
    
    # Incrementa a quantidade do produto
    carrinho[produto_id] += 1
    
    # Converte de volta para JSON e define no cookie com segurança extra
    resp = make_response(redirect(url_for('blueprint_cool.produtos')))
    resp.set_cookie('carrinho', json.dumps(carrinho), max_age=60*60*24, secure=True, httponly=True, samesite='Lax')  # Mais seguro
    
    return resp

# Remover o carrinho
@blueprint_default.route('/remover_carrinho', methods=['POST'])
@login_required
def remover_carrinho():
    resp = make_response(redirect(url_for('blueprint_cool.produtos')))
    resp.set_cookie('carrinho', '', expires=0)  # Remove o cookie do carrinho
    flash('O carrinho foi esvaziado com sucesso!', 'info')
    return resp


# Ver carrinho e calcular o total
@blueprint_default.route('/carrinho')
@login_required
def ver_carrinho():
    carrinho = json.loads(request.cookies.get('carrinho', '{}'))
    total = 0

    # Lista de produtos
    produtos = [
        {'id': '1', 'nome': 'NVIDIA GeForce RTX 3060', 'preco': 2499.90, 'image':'images/rtx3060.jpg'},
        {'id': '2', 'nome': 'AMD Radeon RX 6700 XT', 'preco': 2999.99, 'image':'images/AMD Radeon RX 6700 XT.jfif'},
        {'id': '4', 'nome': 'NVIDIA GeForce RTX 3090', 'preco': 2999.99, 'image':'images/NVIDIA GeForce RTX 3090.jfif'},
        {'id': '3', 'nome': 'NVIDIA GeForce GTX 1660 Super', 'preco': 1799.90, 'image':'images/NVIDIA GeForce GTX 1660 Super.jfif'}
    ]

    # Criar um dicionário de produtos com o id como chave
    produtos_dict = {produto['id']: produto for produto in produtos}

    # Criar uma lista com as informações dos produtos no carrinho
    carrinho_info = []
    for produto_id, quantidade in carrinho.items():
        if produto_id in produtos_dict:
            produto = produtos_dict[produto_id]
            subtotal = produto['preco'] * quantidade
            total += subtotal
            carrinho_info.append({
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': quantidade,
                'subtotal': round(subtotal, 2)  # Exibir subtotal com 2 casas decimais
            })

    # Exibir o total com duas casas decimais
    total = round(total, 2)

    return render_template("carrinho.html", carrinho=carrinho_info, total=total)
