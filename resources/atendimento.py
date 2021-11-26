from flask_restful import Resource, reqparse
import datetime
import sqlite3
from models.atendimento import AtendimentoModel
class FazendoAtendimento(Resource):
    atendimento_dados = reqparse.RequestParser()
    atendimento_dados.add_argument('horario_entrada', type=str, required=True, help='hora_entrada é obrigatorio')
    def post(self, cadastro_pet, tipo_servico):
        dados = FazendoAtendimento.atendimento_dados.parse_args()
        formato = '%H:%M:%S'
        datetime_obj = datetime.datetime.strptime(dados['horario_entrada'], formato)
        atendimento = AtendimentoModel(datetime_obj.time(), 'DATE("now")', cadastro_pet, tipo_servico)
        resultado_json = atendimento.cadastrar_atendimento()
        return resultado_json


class Atendimento(Resource):
    def get(self, atendimento_id):
        atendimento = AtendimentoModel.encontrar_atendimento_por_id(atendimento_id)
        if atendimento:
            return atendimento.json(), 200
        return {'Error': 'atendimento não encontrado'}, 404


class Atendimentos(Resource):
    def get(self):
        consulta_todos_atendimento = "SELECT * FROM TB_ATENDIMENTO"
        connect = sqlite3.connect('banco.db')
        cursor = connect.cursor()
        resultado = cursor.execute(consulta_todos_atendimento)
        atendimentos = []
        for linha in resultado:
            atendimentos.append(
                {
                    'atendimento_id': linha[0],
                    'hora_entrada': linha[1],
                    'hora_saida': linha[2],
                    'data': linha[3],
                    'valor': linha[4],
                    'cpf_profissional': linha[5],
                    'tipo_servico': linha[6]
                }
            )
        return {'messagem': atendimentos}, 200

