import sqlalchemy
from sql_alchemy import banco
from sqlalchemy import types
class PetModel(banco.Model):
    __tablename__ = 'TB_PET'
    cadastro_pet = banco.Column(banco.String(10), primary_key=True)
    nome = banco.Column(banco.String(80))
    data_nascimento = banco.Column(types.Date())
    raca = banco.Column(banco.String(80))
    especie = banco.Column(banco.String(80))
    cpf_cliente = banco.Column(banco.String(12), banco.ForeignKey('TB_CLIENTE.cpf'))
    eh_adotado = banco.Column(banco.Boolean())

    def __init__(self, cadastro_pet, nome, raca, especie):
        self.cadastro_pet = cadastro_pet
        self.nome = nome
        self.raca = raca
        self.especie = especie
        self.eh_adotado = False
        


    @classmethod
    def encontrar_pet_por_cadastro(cls, cadastro_pet):
        pet = cls.query.filter_by(cadastro_pet=cadastro_pet).first()
        if pet:
            return pet
        return None
    
    @classmethod
    def encontrar_pet_por_dono(cls, cpf_cliente):
        pet = cls.query.filter_by(cpf_cliente=cpf_cliente).first()
        if pet:
            return pet
        return None

    def colocar_como_adotado(self, eh_adotado):
        self.eh_adotado = eh_adotado

    def salvar_pet(self):
        banco.session.add(self)
        banco.session.commit()
    
    def deletar_pet(self):
        banco.session.delete(self)
        banco.session.commit()

    def colocar_dono_do_pet(self, cpf):
        self.cpf_cliente = cpf
    
    def colocar_data_nascimento(self, data_nascimento):
        self.data_nascimento = data_nascimento

    def atualizar_pet(self, nome, raca, especie):
        self.nome = nome
        self.raca = raca
        self.especie = especie
    
    def json(self):
        return {
            'cadastro': self.cadastro_pet,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.isoformat(),
            'raca': self.raca,
            'especie': self.especie,
            'cpf_dono': self.cpf_cliente,
            'eh_adotado': self.eh_adotado
        }