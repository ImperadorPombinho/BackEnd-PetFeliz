from flask_restful import Resource, reqparse
import mysql.connector
from models.cliente import ClienteModel
import datetime
from flask_jwt_extended import jwt_required
from models.pet import PetModel


class Pets(Resource):
    def get(self):
        consulta_todos_pets = "SELECT * FROM TB_PET"
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        cursor.execute(consulta_todos_pets)
        resultado = cursor.fetchall()
        pets = []
        if resultado:
            for linha in resultado:
                pets.append(
                    {
                        'cadastro': linha[0],
                        'nome': linha[1],
                        'data_nascimento': str(linha[2]),
                        'raca': linha[3],
                        'especie': linha[4],
                        'cpf_dono': linha[5]
                    }
                )
        return {'pets': pets}, 200


class Pet(Resource):
    pet_dados = reqparse.RequestParser()
    pet_dados.add_argument('nome', type=str, required=True, help='nome é obrigatório')
    pet_dados.add_argument('data_nascimento', type=str, required=True, help='data de nascimento é obrigatória')
    pet_dados.add_argument('raca', type=str, required=True, help='raça é obrigátoria')
    pet_dados.add_argument('especie', type=str, required=True, help='especie é obrigatória')
    pet_dados.add_argument('cpf_cliente', type=str, required=True, help='cpf do dono é obrigatório')
    formato = '%d/%m/%Y'
    def get(self, cadastro_pet):
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if pet:
            return pet.json(), 200
        return {'Error': f'pet {cadastro_pet} não encontrado'}, 404
    
    @jwt_required()
    def post(self, cadastro_pet):
        if PetModel.encontrar_pet_por_cadastro(cadastro_pet):
            return {'Error': 'pet jpa cadastrado'}, 406
        dados = Pet.pet_dados.parse_args()
        dados_sem_cpf_e_sem_data = {chave: valor for chave, valor in dados.items() if chave != 'cpf_cliente' and chave != 'data_nascimento' }
        if not ClienteModel.encontrar_cliente_por_cpf(dados['cpf_cliente']):
            return {'Error': 'se cadastre primeiro para cadastrar seu pet'}, 404
        pet = PetModel(cadastro_pet, **dados_sem_cpf_e_sem_data)
        pet.colocar_dono_do_pet(dados['cpf_cliente'])
        datetime_obj = datetime.datetime.strptime(dados['data_nascimento'], Pet.formato)
        pet.colocar_data_nascimento(datetime_obj.date())
        try:
            pet.salvar_pet()
        except:
            return {'Error': 'erro de servidor'}, 500
            
        return {'messagem': f'cadastro do pet {pet.nome} efetuado com sucesso'}, 201
    
    @jwt_required()
    def put(self, cadastro_pet):
        dados = Pet.pet_dados.parse_args()
        dados_sem_cpf_e_sem_data = {chave: valor for chave, valor in dados.items() if chave != 'cpf_cliente' and chave != 'data_nascimento'}
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if not pet:
            return {'Error': f'pet {pet.nome} não encontrado'}, 404
        pet.atualizar_pet(**dados_sem_cpf_e_sem_data)
        pet.colocar_dono_do_pet(dados['cpf_cliente'])
        datetime_obj = datetime.datetime.strptime(dados['data_nascimento'], Pet.formato)
        pet.colocar_data_nascimento(datetime_obj.date())
        try:
            pet.salvar_pet()
        except:
            return {'Error': 'erro de servidor'}, 500
        return {'messagem': 'alteração de pet feita com sucesso'}, 200

    @jwt_required()
    def delete(self, cadastro_pet):
        pet = PetModel.encontrar_pet_por_cadastro(cadastro_pet)
        if pet:
            try:
                pet.deletar_pet()
            except:
                return {'Error': 'erro ao deletar pet, erro de servidor'}, 500
            return {'messagem': 'pet deletado com sucesso'}, 200
        return {'Error': 'pet nao encontrado'}, 404

    