from flask_restful import Resource, reqparse
from models.carrinho import CarrinhoModel
from models.produto import ProdutoModel



   

class Carrinho(Resource):
    carrinho_dados = reqparse.RequestParser()
    carrinho_dados.add_argument('codigo', type=str, required=True, help='codigo do produto é obrigatorio')
    carrinho_dados.add_argument('quantidade', type=int)
    carrinho_dados.add_argument('cpf_cliente', type=str, required=True, help='cpf do cliente é obrigatório')
    
    def get(self, codigo_carrinho):
        carrinho = CarrinhoModel.encontrar_carrinho_por_codigo(codigo_carrinho)
        if carrinho:
            return carrinho.json(), 200
        return {'Error': f'carrinho {codigo_carrinho} não encontrado'}, 404
    
    def post(self, codigo_carrinho):
        dados = Carrinho.carrinho_dados.parse_args()
        if not CarrinhoModel.encontrar_carrinho_por_codigo(codigo_carrinho):
            carrinho = CarrinhoModel(codigo_carrinho, dados['cpf_cliente'])
            try:
                carrinho.salvar_carrinho()
            except:
                return  {'Error': 'erro de servidor'}, 500
        produto = ProdutoModel.encontrar_produto_por_codigo(dados['codigo'])

        if not produto:
            return {'Error': f'produto {dados["codigo"]} não encontrado '}, 404
        produto.atualizar_produto(quantidade=dados['quantidade'], codigo_carrinho=codigo_carrinho, **produto.json()) 
        produto.salvar_produto()
        return {'messagem': 'produto adicionado no carrinho'}, 200 

    def delete(self, codigo_carrinho):
        carrinho = CarrinhoModel.encontrar_carrinho_por_codigo(codigo_carrinho)
        if carrinho:
            try:
                carrinho.deletar_carrinho()
            except:
                return {'Error': f'erro ao deletar carrinho {codigo_carrinho}, erro de servidor'}, 500
            return {'messagem': 'carrinho deletado com sucesso'}, 200
        return {'Error': f'carrinho {codigo_carrinho} não encontrado'}, 404