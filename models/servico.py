from sql_alchemy import banco


class ServicoModel(banco.Model):
    __tablename__ = 'TB_SERVICO'
    tipo_servico = banco.Column(banco.String(80), primary_key=True)
    preco = banco.Column(banco.Float(precision=2))

    def __init__(self, tipo_servico, preco):
        self.tipo_servico = tipo_servico
        self.preco = preco
    

    @classmethod
    def encontrar_servico_pelo_tipo(cls, tipo_servico):
        servico = cls.query.filter_by(tipo_servico=tipo_servico).first()
        if servico: 
            return servico
        return None

    def salvar_servico(self):
        banco.session.add(self)
        banco.session.commit()
    

    def json(self):
        return {
            'tipo_servico': self.tipo_servico,
            'preco': self.preco
        }
