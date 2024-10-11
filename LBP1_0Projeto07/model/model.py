class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

listaPessoas = []

def addPessoa(nome, idade):
    nova_pessoa = Pessoa(nome, idade)
    listaPessoas.append()