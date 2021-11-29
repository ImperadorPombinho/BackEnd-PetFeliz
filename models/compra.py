from models.carrinho import CarrinhoModel
from models.cliente import ClienteModel
from models.interfaces import InterfaceRegrasNegocio
from sql_alchemy import banco


class CompraModel(banco.Model):
    __tablename__ = 'TB_COMPRA'
    compra_id = banco.Column(banco.Integer(), primary_key=True)
    codigo_carrinho = banco.Column(banco.String(10), banco.ForeignKey('TB_CARRINHO.codigo_carrinho'))
    valor_compra = banco.Column(banco.Float(precision=2))


    def __init__(self, codigo_carrinho):
        self.codigo_carrinho = codigo_carrinho
        self.valor_compra = 0


    @classmethod
    def encontrar_compra_por_id(cls, compra_id):
        compra = cls.query.filter_by(compra_id=compra_id).first()
        if compra:
            return compra
        return None
    
    @classmethod
    def encontrar_compra_por_carrinho(cls, codigo_carrinho):
        compra = cls.query.filter_by(codigo_carrinho=codigo_carrinho)
        if compra:
            return compra
        return None

    def salvar_compra(self):
        banco.session.add(self)
        banco.session.commit() 


    def deletar_compra(self):
        banco.session.delete(self)
        banco.session.commit()


    def realizar_compra(self):
        #função que realiza compra com carrinho
        desconto = 0
        carrinho = CarrinhoModel.encontrar_carrinho_por_codigo(self.codigo_carrinho)
        if not carrinho:
            return {'Error': 'carrinho nao encontrado'}, 404
        lista_produtos = carrinho.pegar_todos_os_produtos()
        valor = 0
        valor_total_compra = 0
        global nao_tem_estoque_no_produto
        nao_tem_estoque_no_produto = False
        for produto in lista_produtos:
            if produto.estoque <= 0:
                nao_tem_estoque_no_produto = True
            valor = produto.preco * produto.quantidade
            valor_total_compra += valor
        if nao_tem_estoque_no_produto:
            return {'Error': 'nao tem estoque no produto'}, 404
        cliente = ClienteModel.encontrar_cliente_por_cpf(carrinho.cpf_cliente)
        if cliente:
            tupla = InterfaceRegrasNegocio.checar_regra_3(cliente.quantidade_gasta)
            desconto = tupla[0]
            cliente.nivel = tupla[1]
            valor_com_desconto = valor_total_compra * desconto
            self.valor_compra = valor_total_compra - valor_com_desconto
            print(self.valor_compra)
            if cliente.creditos >= self.valor_compra:
                cliente.creditos -= self.valor_compra
                cliente.quantidade_gasta += self.valor_compra
                try:
                    cliente.salvar_cliente()
                except:
                    return {'Error': 'erro de servidor'}, 500
                for produto in lista_produtos:
                    quantidade = produto.quantidade
                    produto.estoque -= quantidade
                    try:
                        produto.salvar_produto()
                    except:
                        return {'Error': 'erro de servidorrrr'}, 500
                self.salvar_compra()
                return {'messagem': f'compra do cliente {cliente.cpf} efetuada com sucesso'}, 200
            else:
                return {'messagem': f'creditos faltando'}, 200
        else:
            return {'Error': 'cliente não encontrado'}, 404

    def json(self):
        return {
            'compra_id': self.compra_id,
            'valor_compra': self.valor_compra,
            'codigo_carrinho': self.codigo_carrinho
        }

    
    