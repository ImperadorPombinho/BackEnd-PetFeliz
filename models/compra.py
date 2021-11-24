from models.cliente import ClienteModel
from models.interfaces import InterfaceRegrasNegocio
from models.produto import ProdutoModel
from sql_alchemy import banco


class CompraModel(banco.Model):
    __tablename__ = 'TB_COMPRA'
    compra_id = banco.Column(banco.Integer(), primary_key=True)
    quantidade = banco.Column(banco.Integer())
    data_compra = banco.Column(banco.DATE(tomezone=True))
    horario_compra = banco.Column(banco.TIMESTAMP(timezone=True))
    valor_compra = banco.Column(banco.Float(precision=2))
    codigo = banco.Column(banco.String(10), banco.ForeignKey('TB_PRODUTO.codigo'))
    cpf_cliente = banco.Column(banco.String(12), banco.ForeignKey('TB_CLIENTE.cpf'))


    def __init__(self, quantidade, data_compra, horario_compra, codigo, cpf_cliente):
        self.quantidade = quantidade
        self.data_compra = data_compra
        self.horario_compra = horario_compra
        self.valor_compra = 0
        self.codigo = codigo
        self.cpf_cliente = cpf_cliente

    @classmethod
    def encontrar_compra_por_id(cls, compra_id):
        compra = cls.query.filter_by(compra_id=compra_id).first()
        if compra:
            return compra
        return None
    


    
    def realizar_compra(self):
        desconto = 0.10
        produto = ProdutoModel.encontrar_produto_por_codigo(self.codigo)
        cliente = ClienteModel.encontrar_cliente_por_cpf(self.cpf_cliente)
        if not produto and not cliente:
            return False
        #executar regra de nivel
        #desconto = InterfaceRegrasNegocio.checar_regra_3(cliente)

        valor_compra_total = (produto.preco * self.quantidade)
        valor_desconto_da_compra = valor_compra_total * desconto
        
        self.valor_compra = valor_compra_total - valor_desconto_da_compra
        if cliente.creditos >= self.valor_compra:
            cliente.creditos -= self.valor_compra
            cliente.quantidade_gasta += self.valor_compra
            cliente.atualizar_cliente(**cliente.json())
            try:
                cliente.salvar_cliente() 
            except:
                return False
            return True
        else:
            return False




    def json(self):
        return {
            'compra_id': self.compra_id,
            'quantidade': self.quantidade,
            'data_compra': self.data_compra,
            'horario_compra': self.horario_compra,
            'valor_compra': self.valor_compra,
            'codigo': self.codigo,
            'cpf_cliente': self.cpf_cliente
        }

    
    