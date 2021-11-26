from models.servico import ServicoModel
from sql_alchemy import banco
from sqlalchemy import types
import datetime
class AtendimentoModel(banco.Model):
    __tablename__ = 'TB_ATENDIMENTO'
    atendimento_id = banco.Column(banco.Integer(), primary_key=True)
    hora_entrada = banco.Column(types.TIME(timezone=True))
    hora_saida = banco.Column(types.TIME(timezone=True))
    data = banco.Column(types.Date())
    valor = banco.Column(banco.Float(precision=2))
    cpf_profissional = banco.Column(banco.String(12), banco.ForeignKey('TB_PROFISSIONAL.cpf_profissional'))
    tipo_servico = banco.Column(banco.String(80), banco.ForeignKey('TB_SERVICO.tipo_servico'))
    cadastro_pet = banco.Column(banco.String(10), banco.ForeignKey('TB_PET.cadastro_pet'))

    def __init__(self, hora_entrada, data, cadastro_pet, tipo_servico):
        self.hora_entrada = hora_entrada
        self.hora_saida = None,
        self.data = data
        self.valor = None
        self.tipo_servico = tipo_servico
        self.cadastro_pet = cadastro_pet

    @classmethod
    def encontrar_atendimento_por_id(cls, atendimento_id):
        atendimento = cls.query.filter_by(atendimento_id=atendimento_id).first()
        if atendimento:
            return atendimento
        return None

    def salvar_atendimento(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_atendimento(self):
        banco.session.delete(self)
        banco.session.commit()
    
    def verificar_horario(self, horario_de_entrada):
        formato = '%H:%M:%S'
        hora_saida = ''
        hora_entrada_formatada = str(horario_de_entrada)
        if hora_entrada_formatada == '14:00:00':
            hora_saida = '16:00:00'
            datetime_obj = datetime.datetime.strptime(hora_saida, format)
            self.hora_saida = datetime_obj.time()
        elif hora_entrada_formatada == '17:00:00':
            hora_saida = '19:00:00'
            datetime_obj = datetime.datetime.strptime(hora_saida, horario_de_entrada)
            self.hora_saida = datetime_obj.time()
        elif hora_entrada_formatada == '20:00:00':
            hora_saida = '22:00:00'
            datetime_obj = datetime.datetime.strptime(hora_saida, formato)
            self.hora_saida = datetime_obj.time()

    def cadastrar_atendimento(self):
        self.verificar_horario(self.hora_entrada)
        #realizar regra_1 aqui
        #if profissional == 'Terminou profissionais':
        #   return {'Error': 'todos os profissionais estão trabalhando'}, 404
        servico = ServicoModel.encontrar_servico_pelo_tipo(self.tipo_servico)
        #executar regra 2, ela retorna ja o preço
        
        self.salvar_atendimento()
        return {'messagem': 'atendimento marcado com sucesso'}, 200


    def json(self):
        return {
            'atendimento_id': self.atendimento_id,
            'hora_entrada': self.hora_entrada.isoformat(),
            'hora_saida': self.hora_saida.isoformat(),
            'data': self.data.isoformat(),
            'valor': self.valor,
            'cpf_profissional': self.cpf_profissional,
            'tipo_servico': self.tipo_servico
        }
