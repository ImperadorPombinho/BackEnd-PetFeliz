from logging import fatal
from models.adota import AdotaModel
from models.interfaces import InterfaceRegrasNegocio
from models.pet import PetModel
from models.servico import ServicoModel
from sql_alchemy import banco
from sqlalchemy import types
import mysql.connector
import datetime
class AtendimentoModel(banco.Model):
    __tablename__ = 'TB_ATENDIMENTO'
    atendimento_id = banco.Column(banco.Integer(), primary_key=True)
    atendimento_codigo = banco.Column(banco.String(20))
    hora_entrada = banco.Column(types.TIME(timezone=True))
    hora_saida = banco.Column(types.TIME(timezone=True))
    data = banco.Column(types.Date())
    valor = banco.Column(banco.Float(precision=2))
    cpf_profissional = banco.Column(banco.String(12), banco.ForeignKey('TB_PROFISSIONAL.cpf_profissional'))
    tipo_servico = banco.Column(banco.String(80), banco.ForeignKey('TB_SERVICO.tipo_servico'))
    cadastro_pet = banco.Column(banco.String(10), banco.ForeignKey('TB_PET.cadastro_pet'))

    def __init__(self, atendimento_codigo, hora_entrada, data, cadastro_pet, tipo_servico):
        self.atendimento_codigo = atendimento_codigo
        self.hora_entrada = hora_entrada
        self.hora_saida = None,
        self.data = data
        self.valor = None
        self.tipo_servico = tipo_servico
        self.cadastro_pet = cadastro_pet


    def salvar_atendimento(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_atendimento(self):
        banco.session.delete(self)
        banco.session.commit()
    
    def verificar_horario(self, horario_de_entrada, data, cadastro_pet):
        formato = '%H:%M:%S'
        hora_saida = ''
        consulta_se_ja_tem_data = "SELECT COUNT(*) FROM TB_ATENDIMENTO WHERE DATA = %s AND HORA_ENTRADA = %s AND CADASTRO_PET = %s"
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        cursor.execute(consulta_se_ja_tem_data, (data, horario_de_entrada, cadastro_pet))
        resultado = cursor.fetchall()
        tem_data = False
        if resultado[0][0] == 0 and tem_data == False:
            tem_data = True
        if tem_data:
            hora_entrada_formatada = str(horario_de_entrada)
            if hora_entrada_formatada == '14:00:00':
                hora_saida = '16:00:00'
                datetime_obj = datetime.datetime.strptime(hora_saida, formato)
                self.hora_saida = datetime_obj.time()
            elif hora_entrada_formatada == '17:00:00':
                hora_saida = '19:00:00'
                datetime_obj = datetime.datetime.strptime(hora_saida,formato)
                self.hora_saida = datetime_obj.time()
            elif hora_entrada_formatada == '20:00:00':
                hora_saida = '22:00:00'
                datetime_obj = datetime.datetime.strptime(hora_saida, formato)
                self.hora_saida = datetime_obj.time()
            return True
        return False

    def cadastrar_atendimento(self):
        pode_marcar = self.verificar_horario(self.hora_entrada, self.data, self.cadastro_pet)
        if not pode_marcar:
            return {'Error': 'nao podemos marcar nesta data'}, 500
        profissional_cpf = InterfaceRegrasNegocio.checar_regra_1(self.data)
        if profissional_cpf == '0':
            return {'Error': 'todos os profissionais estão trabalhando'}, 404
        self.cpf_profissional = profissional_cpf
        servico = ServicoModel.encontrar_servico_pelo_tipo(self.tipo_servico)
        if not servico:
            return {'Error': 'não existe esse serviço no catalogo'}, 404
        pet = PetModel.encontrar_pet_por_cadastro(self.cadastro_pet)
        if not pet:
            return {'Error': 'não encontado o pet'}, 404
        self.valor = InterfaceRegrasNegocio.checar_regra_2(self.cadastro_pet, self.tipo_servico)
        return {'messagem': 'atendimento marcado com sucesso'}, 200

    def json(self):
        return {
            'atendimento_id': self.atendimento_id,
            'atendimento_codigo': self.atendimento_codigo,
            'hora_entrada': str(self.hora_entrada),
            'hora_saida': str(self.hora_saida),
            'data': str(self.data),
            'valor': self.valor,
            'cpf_profissional': self.cpf_profissional,
            'tipo_servico': self.tipo_servico
        }
