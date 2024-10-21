import logging
from datetime import datetime

class MeuMiddleware:
    def __init__(self, app, log_ativo=False):  # Adiciona a flag para ativar/desativar logging
        self.app = app
        self.log_ativo = log_ativo  # Define a flag de controle
        if self.log_ativo:
            logging.basicConfig(level=logging.INFO)

    def __call__(self, environ, start_response):
        if self.log_ativo:  # Só faz o logging se a flag estiver True
            inicio = datetime.now()
            metodo = environ.get('REQUEST_METHOD')
            caminho = environ.get('PATH_INFO')
            logging.info(f"Requisição recebida: {metodo} {caminho} às {inicio}")

        # Função para capturar o status da resposta
        def log_status(status, headers, *args):
            if self.log_ativo:
                fim = datetime.now()
                duracao = (fim - inicio).total_seconds()
                logging.info(f"Resposta enviada: {status} | Duração: {duracao:.4f} segundos")
            return start_response(status, headers, *args)

        # Chamar a aplicação com o log da resposta
        response = self.app(environ, log_status)

        if self.log_ativo:
            logging.info(f"Processo concluído para {metodo} {caminho}")
        
        return response
    
class Usuario:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha


# Lista de usuários pré-definidos
usuarios = [Usuario('admin', 'admin'), Usuario('Caique', 'aluno')]
