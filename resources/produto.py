from flask_restful import Resource, reqparse
import mysql.connector

from models.produto import ProdutoModel



class Produtos(Resource):

    def get(self):
        consulta = "SELECT * FROM TB_PRODUTO"
        connect = mysql.connector.connect(user='xsl40cyoa6lt6veb', password='ovg5zexqjxozoggq',  
                                      host='yjo6uubt3u5c16az.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306',
                                      database='f9p7m5j30z3y2jap')
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