from flask import Flask, jsonify
from flask_restful import Api
from resources.adota import Adota
from resources.carrinho import Carrinho
from resources.cliente import Cadastro, Cliente, Clientes, Login, Logout
from resources.compra import Compra
from resources.pet import Pet, Pets
from resources.produto import Produtos, Produto
from excel_dados import preenncher_banco
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def criar_banco():
    banco.create_all()
    preenncher_banco()
    
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'messagem': 'voce ja esta deslogado'}), 401


#rotas da api
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<string:codigo>')
api.add_resource(Cadastro, '/cadastro')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Clientes, '/clientes')
api.add_resource(Cliente, '/clientes/<string:cpf>')
api.add_resource(Carrinho, '/produto/carrinho/<string:codigo_carrinho>')
api.add_resource(Compra, '/carrinho/<string:codigo_carrinho>/compra')
api.add_resource(Pets, '/pets')
api.add_resource(Pet, '/pet/<string:cadastro_pet>')
api.add_resource(Adota, '/cliente/<string:cpf_cliente>/adota/pet/<string:cadastro_pet>')

#http://127.0.0.1:5000/ -> rota raiz

# main do projeto
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

