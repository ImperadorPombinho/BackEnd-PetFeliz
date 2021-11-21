from flask_restful import Resource, reqparse
import sqlite3

consulta = 'SELECT * FROM TB_PRODUTOS'

class Produtos(Resource):

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        resultado = cursor.execute(consulta)
        produtos = []
        for linha in resultado:
            produtos.append(
                {
                    'codigo': linha[0],
                    'nome': linha[1],
                    'tipo': linha[2],
                    'preco': linha[3],
                    'estoque': linha[4]
                }
            )

        return {'produtos': produtos}
