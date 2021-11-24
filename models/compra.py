from models.interfaces import InterfaceRegrasNegocio
from sql_alchemy import banco


class CompraModel(banco.Model):
    __tablename__ = 'TB_COMPRA'
    compra_id = banco.Column(banco.Integer(), primary_key=True)
    data_compra = banco.Column(banco.DATE(tomezone=True))
    horario_compra = banco.Column(banco.TIMESTAMP(timezone=True))
    valor_compra = banco.Column(banco.Float(precision=2))
    codigo = banco.Column(banco.String(10), banco.ForeignKey('TB_CARRINHO.codigo_carrinho'))


    def __init__(self, data_compra, horario_compra, codigo_carrinho):
        self.data_compra = data_compra
        self.horario_compra = horario_compra
        self.valor_compra = 0
        self.codigo_carrinho = codigo_carrinho

    @classmethod
    def encontrar_compra_por_id(cls, compra_id):
        compra = cls.query.filter_by(compra_id=compra_id).first()
        if compra:
            return compra
        return None
    


    
    def realizar_compra(self):
        #função que realiza a compra com carrinho
        pass




    def json(self):
        return {
            'compra_id': self.compra_id,
            'quantidade': self.quantidade,
            'data_compra': self.data_compra,
            'horario_compra': self.horario_compra,
            'valor_compra': self.valor_compra,
            'codigo_carrinho': self.codigo_carrinho
        }

    
    