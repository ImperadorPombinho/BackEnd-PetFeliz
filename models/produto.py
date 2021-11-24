from sql_alchemy import banco


class ProdutoModel(banco.Model):
    __tablename__ = 'TB_PRODUTO'
    codigo = banco.Column(banco.String(10), primary_key=True)
    nome = banco.Column(banco.String(70))
    tipo = banco.Column(banco.String(60))
    preco = banco.Column(banco.Float(precision=2))
    estoque = banco.Column(banco.Integer())
    quantidade = banco.Column(banco.Integer())
    codigo_carrinho = banco.Column(banco.String(10), banco.ForeignKey('TB_CARRINHO.codigo_carrinho'))

    def __init__(self, codigo, nome, tipo, preco, estoque):
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
        self.estoque = estoque
        self.quantidade = 1
    
    @classmethod
    def encontrar_produto_por_codigo(cls, codigo):
        produto = cls.query.filter_by(codigo=codigo).first()
        if produto:
            return produto
        return None

    def salvar_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_produto(self):
        banco.session.delete(self)
        banco.session.commit()

    def atualizar_produto(self, nome, tipo, preco, estoque, quantidade, codigo_carrinho):
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
        self.estoque = estoque
        self.quantidade = quantidade
        self.codigo_carrinho = codigo_carrinho

    def json(self):
        return {
            'nome': self.nome,
            'tipo': self.tipo,
            'preco': self.preco,
            'estoque': self.estoque
        }


    