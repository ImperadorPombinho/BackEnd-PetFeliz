from flask_restful import Resource, reqparse
import sqlite3



class Clientes(Resource):
    def get(self):
        consulta_todos_clientes = "SELECT CPF, NOME, RG, TELEFONE, ENDERECO, EMAIL, QUANTIDADE_GASTA, CREDITOS FROM TB_CLIENTE"
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        resultado_consulta = cursor.execute(consulta_todos_clientes)
        clientes = []
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