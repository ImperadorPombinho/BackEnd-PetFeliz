from flask_restful import Resource
from flask import send_from_directory
from file import DIRETORIO_DOWNLOAD




class Download(Resource):
    def get(self, nome_arquivo):
        return send_from_directory(DIRETORIO_DOWNLOAD, nome_arquivo, as_attachment=True)