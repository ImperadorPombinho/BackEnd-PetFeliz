from models.cliente import ClienteModel
from models.pet import PetModel
from sql_alchemy import banco
from sqlalchemy import types

class AdotaModel(banco.Model):
    __tablename__ = 'TB_ADOTA'
    adota_id = banco.Column(banco.Integer(), primary_key=True)
    data_adocao = banco.Column(types.Date())
    horario_adocao = banco.Column(types.TIME(timezone=True))
    cadastro_pet = banco.Column(banco.String(10), banco.ForeignKey('TB_PET.cadastro_pet'))
    cpf_cliente = banco.Column(banco.String(12), banco.ForeignKey('TB_CLIENTE.cpf'))

    def __init__(self, data_adocao, horario_adocao, cadastro_pet, cpf_cliente):
        self.data_adocao = data_adocao
        self.horario_adocao = horario_adocao
        self.cadastro_pet = cadastro_pet
        self.cpf_cliente = cpf_cliente
    
    @classmethod
    def encontrar_adocao_por_pet(cls, cadastro_pet):
        adocao = cls.query.filter_by(cadastro_pet=cadastro_pet).first()
        if adocao:
            return adocao
        return None

    @classmethod
    def encontrar_adocao_por_cliente(cls, cpf_cliente):
        adocao = cls.query.filter_by(cpf_cliente=cpf_cliente).first()
        if adocao:
            return adocao
        return None  
    
    def realizar_adocao(self):
        pet = PetModel.encontrar_pet_por_cadastro(self.cadastro_pet)
        cliente = ClienteModel.encontrar_cliente_por_cpf(self.cpf_cliente)
        if not cliente:
            return {'Error': 'cliente não encontrado'}, 404
        if not pet:
            return {'Error': 'pet não encontrado'}, 404
        
        if pet.eh_adotado:
            pet.colocar_dono_do_pet(self.cpf_cliente)
            pet.colocar_como_adotado(False)
            pet.salvar_pet()
            self.salvar_adota()
            return {'messagem': 'adoção feita com sucesso'}, 200
        return {'Error': 'pet ja tem dono'}, 500
        


    def salvar_adota(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_adota(self):
        banco.session.delete(self)
        banco.session.commit()
    
    def json(self):
        return {
            'adota_id': self.adota_id,
            'data_adocao': str(self.data_adocao),
            'horario_adocao': str(self.data_adocao),
            'cadastro_pet': self.cadastro_pet,
            'cpf_cliente': self.cpf_cliente
        }
    