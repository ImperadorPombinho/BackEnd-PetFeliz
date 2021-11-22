from flask_restful import Resource, reqparse
import sqlite3

from models.produto import ProdutoModel

consulta = 'SELECT * FROM produto'

class Produtos(Resource):

    def get(self):
        

        return {'produtos': [produtos.json() for produtos in ProdutoModel.query.all()]}
