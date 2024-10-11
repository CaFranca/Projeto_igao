#class Pessoa:
#    def __init__(self, nome, idade):
#       self.nome = nome
#      self.idade = idade

#listaPessoas = []

#def addPessoa(nome, idade):
#   nova_pessoa = Pessoa(nome, idade)
#    listaPessoas.append()



class Usuario:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

class MeuMiddleware:
    def __init__(self, app):
        self.app=app
    def __call__(self, environ, start_response):
        print("Antes da Requesição")
        return self.app(environ,start_response)
    



usuarios = [Usuario('admin','admin'), Usuario('Caique','aluno')]

