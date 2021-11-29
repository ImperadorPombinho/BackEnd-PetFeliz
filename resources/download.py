from flask_restful import Resource
from flask import send_from_directory
from file import DIRETORIO_DOWNLOAD
from flask_jwt_extended import jwt_required



class Download(Resource):
    
    @jwt_required()
    def get(self, nome_arquivo):
        return send_from_directory(DIRETORIO_DOWNLOAD, nome_arquivo, as_attachment=True)