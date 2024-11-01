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
usuarios = [Usuario('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
            Usuario('Caique', 'a21d6f3803f0491c32444ef91a0836be243cc4da5186357e805b7009a5b0669b'),
            Usuario('Absolute', "89ec0bb81771a4212cb70663681fbe4f990f4aeea8fd455fe6ed5bd0badce2fa")]
