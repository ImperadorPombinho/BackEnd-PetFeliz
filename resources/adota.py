from flask_restful import Resource, reqparse

from models.adota import AdotaModel


class Adota(Resource):
    def post(self, cpf_cliente, cadastro_pet):
        adota = AdotaModel('SYSDATE()', 'NOW()', cadastro_pet, cpf_cliente)
        resultado_json = adota.realizar_adocao()
        return resultado_json
