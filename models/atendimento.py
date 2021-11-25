from sql_alchemy import banco
from sqlalchemy import types

class AtendimentoModel(banco.Model):
    __tablename__ = 'TB_ATENDIMENTO'
    atendimento_id = banco.Column(banco.Integer(), primary_key=True)
    hora_entrada = banco.Column(types.TIMESTAMP(timezone=True))
    hora_saida = banco.Column(types.TIMESTAMP(timezone=True))
    data = banco.Column(types.Date())
    valor = banco.Column(banco.Float(precision=2))
    cpf_profissional = banco.Column(banco.String(12), banco.ForeignKey('TB_PROFISSIONAL.cpf_profissional'))
    tipo_servico = banco.Column(banco.String(80), banco.ForeignKey('TB_SERVICO.tipo_servico'))


    def __init__(self, hora_entrada, hora_saida, data, cpf_profissional, tipo_servico):
        self.hora_entrada = hora_entrada
        self.hora_saida = hora_saida,
        self.data = data
        self.valor = 0
        self.cpf_profissional = cpf_profissional
        self.tipo_servico = tipo_servico

    @classmethod
    def encontrar_atendimento_por_id(cls, atendimento_id):
        atendimento = cls.query.filter_by(atendimento_id=atendimento_id).first()
        if atendimento:
            return atendimento
        return None

    def salvar_atendimento(self):
        banco.session.add(self)
        banco.session.commit()


    def json(self):
        return {
            'atendimento_id': self.atendimento_id,
            'hora_entrada': self.hora_entrada,
            'hora_saida': self.hora_saida,
            'data': self.data,
            'valor': self.valor,
            'cpf_profissional': self.cpf_profissional,
            'tipo_servico': self.tipo_servico
        }
