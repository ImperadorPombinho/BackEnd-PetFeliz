

class ClienteModel:

    def __init__(self, cpf, nome, rg, telefone, endereco, email, senha, creditos):
        self.cpf = cpf
        self.nome = nome
        self.rg = rg
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.quantidade_gasta = 0
        self.creditos = creditos

        pass

