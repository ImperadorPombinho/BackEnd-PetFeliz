from sql_alchemy import banco
from sqlalchemy import types

class ProfissionalModel(banco.Model):
    __tablename__ = 'TB_PROFISSIONAL'
    cpf_profissional = banco.Column(banco.String(12), primary_key=True)
    nome = banco.Column(banco.String(80))
    endereco = banco.Column(banco.String(80))
    telefone = banco.Column(banco.String(20))
    data_nascimento = banco.Column(types.Date())


    def __init__(self, cpf_profissional, nome, endereco, telefone, data_nascimento):
        self.cpf_profissional = cpf_profissional
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.data_nascimento = data_nascimento

    
    @classmethod
    def encontrar_profissional_por_cpf(cls, cpf_profissional):
        profissional = cls.quety.filter_by(cpf_profissional=cpf_profissional).first()
        if profissional:
            return profissional
        return None

    def salvar_profissional(self):
        banco.session.add(self)
        banco.session.commit()

    
    
    def json(self):
        return {
            'cpf_profissional': self.cpf_profissional,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'data_nascimento': str(self.data_nascimento)
        }
        
