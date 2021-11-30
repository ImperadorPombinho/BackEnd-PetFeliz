import mysql.connector


class InterfaceRegrasNegocio:
    
    
                
    @classmethod
    def checar_regra_3(cls, quantidade_gasta):
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        regra_3 = "SET @REGRA3 = REGRA_3(%s)"
        cursor.execute(regra_3, (quantidade_gasta,))
        pegar_resultado = "SELECT @REGRA3"
        cursor.execute(pegar_resultado)
        resultado = cursor.fetchall()
        nivel = str(resultado[0][0])
        if nivel == 'Sem Nivel':
            return 0, nivel
        elif nivel == 'Filhote':
            return 0.05, nivel
        elif nivel == 'Mascote':
            return 0.10, nivel
        else:
            return 0.15, nivel
    
    @classmethod
    def checar_regra_2(cls, codigo, tipo):
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        regra_2 = "SET @REGRA2 = REGRA_2(%s, %s)"
        cursor.execute(regra_2, (codigo, tipo))
        pegar_resultado = "SELECT @REGRA2"
        cursor.execute(pegar_resultado)
        resultado = cursor.fetchall() 
        return resultado[0][0]

    @classmethod
    def checar_regra_1(cls, data_atendimento):
        connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
        cursor = connect.cursor()
        regra_1 = "SET @REGRA1 = REGRA_1(%s)"
        cursor.execute(regra_1, (data_atendimento,))
        pegar_resultado = "SELECT @REGRA1"
        cursor.execute(pegar_resultado)
        resultado = cursor.fetchall()
        return resultado[0][0]
