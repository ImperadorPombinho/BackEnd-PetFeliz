import mysql.connector


class InterfaceRegrasNegocio:
    regra_1 = 'SET @REGRA1 = REGRA_1(%s); \
                SELECT @REGRA1;'
    regra_2 = 'SET @REGRA2 = REGRA_2(%s, %s); \
                SELECT @REGRA2;'
    regra_3 = 'SET @REGRA3 = REGRA_3(%s); \
                SELECT @REGRA3;'
    @classmethod
    def checar_regra_3(cls, quantidade_gasta):
        connect = mysql.connector.connect(user='root', password='0',
                                      host='localhost:3306',
                                      database='the_drungas')
        cursor = connect.cursor()
        cursor.execute(InterfaceRegrasNegocio.regra_1, [quantidade_gasta])
        resultado = cursor.fetchall()
        nivel = resultado[0][0]
        if nivel == 'Sem nivel':
            return 0, nivel
        elif nivel == 'Filhote':
            return 0.05, nivel
        elif nivel == 'Mascote':
            return 0.10, nivel
        else:
            return 0.15, nivel
    
    @classmethod
    def checar_regra_2(cls, codigo, tipo):
        connect = mysql.connector.connect(user='root', password='0',
                                      host='localhost:3306',
                                      database='the_drungas')
        cursor = connect.cursor()
        cursor.execute(InterfaceRegrasNegocio.regra_2, [codigo, tipo])
        resultado = cursor.fetchall()
        return resultado[0][0]

    @classmethod
    def checar_regra_1(cls, data_atendimento):
        connect = mysql.connector.connect(user='root', password='0',
                                      host='localhost:3306',
                                      database='the_drungas')
        cursor = connect.cursor()
        cursor.execute(InterfaceRegrasNegocio.regra_3, [data_atendimento])
        resultado = cursor.fetchall()
        return resultado[0][0]
