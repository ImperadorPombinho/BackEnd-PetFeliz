from sql_alchemy import banco


class CarrinhoModel(banco.Model):
    __tablename__ = 'TB_CARRINHO'
    codigo_carrinho = banco.Column(banco.String(10), primary_key=True)
    cpf_cliente = banco.Column(banco.String(12), banco.ForeignKey('TB_CLIENTE.cpf'))
    produtos = banco.relationship('ProdutoModel')

    def __init__(self,codigo_carrinho, cpf_cliente):
        self.codigo_carrinho = codigo_carrinho
        self.cpf_cliente = cpf_cliente
    
    def salvar_carrinho(self):
        banco.session.add(self)
        banco.session.commit()
    
    def deletar_carrinho(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def encontrar_carrinho_por_codigo(cls, codigo_carrinho):
        carrinho = cls.query.filter_by(codigo_carrinho=codigo_carrinho).first()
        if carrinho:
            return carrinho
        return None

    def atualizar_carrinho(self, cpf_cliente):
        self.cpf_cliente = cpf_cliente

    def pegar_todos_os_produtos(self):
        lista = [produto for produto in self.produtos]
        return lista
    
    def json(self):
        return {
            'codigo_carrinho': self.codigo_carrinho,
            'cpf_cliente': self.cpf_cliente,
            'produtos': [produto.json() for produto in self.produtos]
        }
