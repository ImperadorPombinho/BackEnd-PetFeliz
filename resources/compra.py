from flask_restful import Resource
from models.compra import CompraModel


class Compra(Resource):
    def get(self, codigo_carrinho):
        compra = CompraModel.encontrar_compra_por_carrinho(codigo_carrinho)
        if compra:
            return compra.json(), 200
        return {'Error': 'compra  não encontrada'}, 404

    def post(self, codigo_carrinho):
        compra = CompraModel(codigo_carrinho)
        retorno_json = compra.realizar_compra()
        return retorno_json

    def delete(self, codigo_carrinho):
        compra = CompraModel.encontrar_compra_por_carrinho(codigo_carrinho)
        if compra:
            try:
                compra.deletar_compra()
            except:
                return {'Error': 'erro ao deletar conta, erro de servidor'}, 500
            return {'messagem': 'compra deletada com sucesso'}, 200
        return {'Error': 'compra não encontrada'}, 404