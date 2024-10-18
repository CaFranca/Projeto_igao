class Usuario:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

class MeuMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print("Antes da Requisição")
        response = self.app(environ, start_response)
        print("Após a Requisição")  # Logging pós-resposta
        return response

# Lista de usuários pré-definidos
usuarios = [Usuario('admin', 'admin'), Usuario('Caique', 'aluno')]
