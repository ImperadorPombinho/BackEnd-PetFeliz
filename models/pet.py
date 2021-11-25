from sql_alchemy import banco

class PetModel(banco.Model):
    __tablename__ = 'TB_PET'
    cadastro_pet = banco.Column(banco.String(10), primary_key=True)
    nome = banco.Column(banco.String(80))
    data_nascimento = banco.Column(banco.DateTime(timezone=True))
    raca = banco.Column(banco.String(80))
    especie = banco.Column(banco.String(80))
    cpf_cliente = banco.Column(banco.String(12), banco.ForeignKey('TB_CLIENTE.cpf'))

    def __init__(self, cadastro_pet, nome, data_nascimento, raca, especie):
        self.cadastro_pet = cadastro_pet
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.raca = raca
        self.especie = especie


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

    def salvar_pet(self):
        banco.session.add(self)
        banco.session.commit()
    
    def deletar_pet(self):
        banco.session.delete(self)
        banco.session.commit()

    def colocar_dono_do_pet(self, cpf):
        self.cpf_cliente = cpf

    def atualizar_pet(self, nome, data_nascimento, raca, especie):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.raca = raca
        self.especie = especie
    
    def json(self):
        return {
            'cadastro': self.cadastro_pet,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'raca': self.raca,
            'especie': self.especie,
            'cpf_dono': self.cpf_cliente
        }