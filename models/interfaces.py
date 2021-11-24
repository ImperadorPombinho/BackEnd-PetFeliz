import sqlite3


class InterfaceRegrasNegocio:
    regra_1 = 'EXECUTE REGRA_1'
    regra_2 = 'EXECUTE REGRA_2'
    regra_3 = 'EXECUTE REGRA_3'
    @classmethod
    def checar_regra_3(cls, cliente):
        connect = sqlite3.connect('banco.db')
        cursor = connect.cursor()
        resultado = cursor.execute(InterfaceRegrasNegocio.regra_1, [cliente.quantidade_gasta, cliente.cpf])
        if cliente.nivel == 'Sem nivel':
            return 0
        elif cliente.nivel == 'Filhote':
            return 0.05
        elif cliente.nivel == 'Mascote':
            return 0.10
        else:
            return 0.15
    
    @classmethod
    def checar_regra_2(cls, codigo, tipo):
        connect = sqlite3.connect('banco.db')
        cursor = connect.cursor()
        cursor.execute(InterfaceRegrasNegocio.regra_2, [codigo, tipo])


    @classmethod
    def checar_regra_1(cls):
        connect = sqlite3.connect('banco.db')
        cursor = connect.cursor()
        cursor.execute(InterfaceRegrasNegocio.regra_1)
    
