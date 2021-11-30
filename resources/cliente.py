from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_jwt_extended.utils import get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import mysql.connector
from models.cliente import ClienteModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('cpf', type=str, required=True, help="Cpf é obrigatorio")
argumentos.add_argument('nome', type=str, required=True, help="nome é obrigatorio")
argumentos.add_argument('rg', type=str, required=True, help="rg é obrigatorio")
argumentos.add_argument('telefone', type=str, required=True, help="telefone é obrigatorio")
argumentos.add_argument('endereco', type=str, required=True, help="endereco é obrigatorio")
argumentos.add_argument('email', type=str, required=True, help="email é obrigatorio")
argumentos.add_argument('senha', type=str, required=True, help="senha é obrigatorio")
argumentos.add_argument('creditos', type=float, required=True, help="creditos é obrigatorio")
class Clientes(Resource):
    def get(self):
        consulta_todos_clientes = "SELECT CPF, NOME, RG, TELEFONE, ENDERECO, EMAIL, QUANTIDADE_GASTA, CREDITOS FROM TB_CLIENTE"
        connect = mysql.connector.connect(user='root', password='0',
                                      database='the_drungas')
        cursor = connect.cursor()
        cursor.execute(consulta_todos_clientes)
        resultado_consulta = cursor.fetchall()
        clientes = []
        if resultado_consulta:
            for linha in resultado_consulta:
                clientes.append(
                    {
                        'cpf': linha[0],
                        'nome': linha[1],
                        'rg': linha[2],
                        'telefone': linha[3],
                        'endereco': linha[4],
                        'email': linha[5],
                        'quantidade_gasta': linha[6],
                        'creditos': linha[7]
                    }
                )

        return {'clientes': clientes}, 200

class Cliente(Resource):
    cliente_atualiza = reqparse.RequestParser()
    cliente_atualiza.add_argument('nome', type=str, required=True, help="nome é obrigatorio")
    cliente_atualiza.add_argument('rg', type=str, required=True, help="rg é obrigatorio")
    cliente_atualiza.add_argument('telefone', type=str, required=True, help="telefone é obrigatorio")
    cliente_atualiza.add_argument('endereco', type=str, required=True, help="endereco é obrigatorio")
    cliente_atualiza.add_argument('email', type=str, required=True, help="email é obrigatorio")
    cliente_atualiza.add_argument('senha', type=str, required=True, help="senha é obrigatorio")
    cliente_atualiza.add_argument('creditos', type=float, required=True, help="creditos é obrigatorio")
    def get(self, cpf):
        cliente = ClienteModel.encontrar_cliente_por_cpf(cpf)
        if cliente:
            return cliente.json(), 200
        return {'Error': 'Cliente não encontrado'}, 404
    
    
    def put(self, cpf):
        dados = Cliente.cliente_atualiza.parse_args()

        cliente = ClienteModel.encontrar_cliente_por_cpf(cpf)
        if cliente:
            try:
                cliente.atualizar_cliente(cpf=cliente.get_cpf(), quantidade_gasta=cliente.get_quantidade_gasta(), **dados)
                cliente.salvar_cliente()
                return cliente.json(), 200
            except:
                return {'Error': 'erro ao atualizar, erro de servidor'}, 500
        return {'Error': f'erro ao atualizar cliente {cpf}, cliente nao encontrado'}, 404
    
    
    def delete(self, cpf):
        cliente_a_deletar = ClienteModel.encontrar_cliente_por_cpf(cpf)
        if cliente_a_deletar:
            try:
                cliente_a_deletar.deletar_cliente()
            except:
                return {'Error': f'nao conseguimos deletar o cliente {cpf}, problema de servidor'}, 500
            return {'messagem': f'cliente {cpf} foi deletado com sucesso'}, 200
        return {'Error': f'cliente {cpf} não existe'}, 404

class Cadastro(Resource):
    def post(self):
        dados = argumentos.parse_args()
        if (ClienteModel.encontrar_cliente_por_cpf(dados['cpf']) or 
        ClienteModel.encontrar_cliente_por_email(dados['email']) or
        ClienteModel.encontrar_cliente_por_rg(dados['rg'])):
            return {'Error': f'cliente {dados["cpf"]} já existe'}, 404
        cliente_a_criar = ClienteModel(**dados)
        try:
            cliente_a_criar.salvar_cliente()
        except:
            return {'Error': f'nao conseguimos criar o cliente {dados["cpf"]}, problema no servidor'}, 500
        return {'messagem': f'cliente {dados["cpf"]} criado com sucesso'}, 200


class Login(Resource):
    login_dados = reqparse.RequestParser()
    login_dados.add_argument('email', type=str, required=True, help="Email é obrigatorio")
    login_dados.add_argument('senha', type=str, required=True, help='Senha é obrigatoria')
    
    @classmethod
    def post(cls):
        dados = Login.login_dados.parse_args()
        cliente = ClienteModel.encontrar_cliente_por_email(dados['email'])
        if cliente and safe_str_cmp(cliente.get_senha(), dados['senha']):
            cria_token = create_access_token(identity=cliente.get_cpf())
            return {'token_de_acesso': cria_token}, 200
        return {'Error': 'seu login ou senha estão incorretos'}, 401

class Logout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'messagem': 'você foi deslogado com sucesso'}, 200