from datetime import date, time
from flask_restful import Resource, reqparse

from models.compra import CompraModel


class Compra(Resource):
    compra_dados = reqparse.RequestParser()
    compra_dados.add_argument('data_compra', type=date, required=True, help='Data é obrigatória')
    compra_dados.add_argument('horario_compra', type=time, required=True, help='Horario é obrigatorio')
    def get(self, codigo_carrinho):
        compra = CompraModel.encontrar_compra_por_carrinho(codigo_carrinho)
        if compra:
            return compra.json(), 200
        return {'Error': f'compra {compra.compra_id} não encontrada'}, 404

    def post(self, codigo_carrinho):
        COMANDO = 'SYSDATE' #ve se esse comando aceita
        compra = CompraModel(codigo_carrinho, COMANDO, COMANDO)
        retorno_json = compra.realizar_compra()
        return retorno_json

    def delete(self, codigo_carrinho):
        compra = CompraModel.encontrar_compra_por_carrinho(codigo_carrinho)
        if compra:
            try:
                compra.deletar_conta()
            except:
                return {'Error': 'erro de servidor'}, 500
            return {'messagem': 'compra deletada com sucesso'}, 200
        return {'Error': 'compra não encontrada'}, 404