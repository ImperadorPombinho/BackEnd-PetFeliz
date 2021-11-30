from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import datetime
import mysql.connector
from models.atendimento import AtendimentoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('data_atendimento', type=str)
class FazendoAtendimento(Resource):
    atendimento_dados = reqparse.RequestParser()
    atendimento_dados.add_argument('horario_entrada', type=str, required=True, help='hora_entrada é obrigatorio')
    atendimento_dados.add_argument('data', type=str, required=True, help='data atendimento é obrigatorio')
    
    @jwt_required()
    def post(self, cadastro_pet, tipo_servico):
        dados = FazendoAtendimento.atendimento_dados.parse_args()
        formato = '%H:%M:%S'
        formato_data = '%d/%m/%Y'
        atendimento_codigo = str(cadastro_pet) + str(tipo_servico)
        datetime_obj = datetime.datetime.strptime(dados['horario_entrada'], formato)
        datetime_obj_2 = datetime.datetime.strptime(dados['data'], formato_data)
        atendimento = AtendimentoModel(atendimento_codigo, datetime_obj.time(), datetime_obj_2.date(), cadastro_pet, tipo_servico)
        resultado_json = atendimento.cadastrar_atendimento()
        if resultado_json[1] == 200:
            atendimento.salvar_atendimento()
        return resultado_json


class Atendimento(Resource):
    def get(self, atendimento_codigo):
        dados = argumentos.parse_args()
        lista_atendimento = []
        if dados['data_atendimento']:
            formato = '%d/%m/%Y'
            datetime_obj = datetime.datetime.strptime(dados['data_atendimento'], formato)
            datas = datetime.timedelta.resolution
            connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
            cursor = connect.cursor()
            consulta_com_data =  "SELECT * FROM TB_ATENDIMENTO WHERE DATA = %s AND ATENDIMENTO_CODIGO = %s"
            cursor.execute(consulta_com_data, (datetime_obj.date(), atendimento_codigo))
            resultado = cursor.fetchall()
            
            if resultado:
                for linha in resultado:
                    lista_atendimento.append(
                        {
                            'atendimento_id': linha[0],
                            'atendimento_codigo': linha[1],
                            'hora_entrada': str(linha[2]),
                            'hora_saida': str(linha[3]),
                            'data': str(linha[4]),
                            'valor': linha[5],
                            'cpf_profissional': linha[6],
                            'tipo_servico': linha[7]
                        }
                    )
            return {'messagem': lista_atendimento}, 200
        else:   
            connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
            cursor = connect.cursor()
            consulta_sem_data =  "SELECT * FROM TB_ATENDIMENTO WHERE ATENDIMENTO_CODIGO = %s"
            cursor.execute(consulta_sem_data, (atendimento_codigo,))
            resultado = cursor.fetchall()
            if resultado:
                for linha in resultado:
                    lista_atendimento.append(
                        {
                            'atendimento_id': linha[0],
                            'atendimento_codigo': linha[1],
                            'hora_entrada': str(linha[2]),
                            'hora_saida': str(linha[3]),
                            'data': str(linha[4]),
                            'valor': linha[5],
                            'cpf_profissional': linha[6],
                            'tipo_servico': linha[7]
                        }
                    )
            return {'messagem': lista_atendimento}, 200




