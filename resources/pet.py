from sqlite3.dbapi2 import Date
from flask_restful import Resource, reqparse
import sqlite3
from models.cliente import ClienteModel

from models.pet import PetModel


class Pets(Resource):
    def get(self):
        consulta_todos_pets = "SELECT * FROM TB_PET"
        connect = sqlite3.connect('banco.db')
        cursor = connect.cursor()
        resultado = cursor.execute(consulta_todos_pets)
        pets = []
        for linha in resultado:
            pets.append(
                {
                    'cadastro': linha[0],
                    'nome': linha[1],
                    'data_nascimento': linha[2],
                    'raca': linha[3],
                    'especie': linha[4],
                    'cpf_dono': linha[5]
                }
            )
        return {'pets': pets}, 200


class Pet(Resource):
    pet_dados = reqparse.RequestParser()
    pet_dados.add_argument('nome', type=str, required=True, help='nome é obrigatório')
    pet_dados.add_argument('data_nascimento', type=Date, required=True, help='data de nascimento é obrigatória')
    pet_dados.add_argument('raca', type=str, required=True, help='raça é obrigátoria')
    pet_dados.add_argument('especie', type=str, required=True, help='especie é obrigatória')
    pet_dados.add_argument('cpf_cliente', type=str, required=True, help='cpf do dono é obrigatório')
    
    def get(self, cadastro_pet):
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if pet:
            return pet.json(), 200
        return {'Error': f'pet {cadastro_pet} não encontrado'}, 404

    def post(self, cadastro_pet):
        dados = Pet.pet_dados.parse_args()
        if not ClienteModel.encontrar_cliente_por_cpf(dados['cpf_cliente']):
            return {'Error': 'se cadastre primeiro para cadastrar seu pet'}, 404
        pet = PetModel(cadastro_pet, **dados)
        try:
            pet.salvar_pet()
        except:
            return {'Error': 'erro de servidor'}, 500
        return {'messagem': f'cadastro do pet {pet.nome} efetuado com sucesso'}, 200
    
    def put(self, cadastro_pet):
        dados = Pet.pet_dados.parse_args()
        dados_sem_cpf = {chave: valor for chave, valor in dados.items() if not dados.get('cpf_cliente')}
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if not pet:
            return {'Error': f'pet {pet.nome} não encontrado'}, 404
        try:
            pet.atualizar_pet(**dados_sem_cpf)
            pet.salvar_pet()
        except:
            return {'Error': 'erro ao alterar pet, erro de servidor'}, 500
        return {'messagem': 'alteração de pet feita com sucesso'}, 200


    def delete(self, cadastro_pet):
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if pet:
            try:
                pet.deletar_pet()
            except:
                return {'Error': 'erro ao deletar pet, erro de servidor'}, 500
            return {'messagem': 'pet deletado com sucesso'}, 200
        return {'Error': 'pet nao encontrado'}, 404

    