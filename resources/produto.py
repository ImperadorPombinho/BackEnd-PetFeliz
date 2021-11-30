from flask_restful import Resource, reqparse
import mysql.connector

from models.produto import ProdutoModel



class Produtos(Resource):

    def get(self):
        consulta = "SELECT * FROM TB_PRODUTO"
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        produtos = []

        for linha in resultado:
            produtos.append(
                {
                    'codigo': linha[0],
                    'nome': linha[1],
                    'tipo': linha[2],
                    'preco': linha[3],
                    'estoque': linha[4],
                    'quantidade': linha[5]
                }
            )
        return {'produtos': produtos}, 200


class Produto(Resource):

    def get(self, codigo):
        produto = ProdutoModel.encontrar_produto_por_codigo(codigo)
        if produto:
            return produto.json(), 200
        return {'Error': f'Nao encontrado produto: {codigo}'}, 404