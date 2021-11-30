def criar_regras():
    import mysql.connector
    regra_1 = "create  function REGRA_1( \
pDATA_ATENDIMENTO DATE \
) \
returns VARCHAR(20) \
deterministic \
begin \
    declare vCPF VARCHAR(20); \
    declare vCPF_AUX VARCHAR(20); \
    declare ACABOU int DEFAULT FALSE; \
    declare cPROFISSIONAL CURSOR FOR SELECT CPF_PROFISSIONAL FROM TB_PROFISSIONAL; \
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET ACABOU = TRUE; \
    SELECT COUNT(*) INTO @vCONT FROM TB_ATENDIMENTO WHERE DATA = pDATA_ATENDIMENTO; \
    SET vCPF = '0'; \
    OPEN cPROFISSIONAL; \
    IF @vCONT <= 0 THEN \
        loop_sem_atendimento: LOOP \
            FETCH cPROFISSIONAL INTO vCPF_AUX; \
            IF ACABOU THEN \
            LEAVE loop_sem_atendimento; \
            END IF; \
            SET vCPF = vCPF_AUX; \
        END LOOP loop_sem_atendimento; \
    ELSE \
        loop_com_atendimento: LOOP \
            FETCH cPROFISSIONAL INTO vCPF_AUX; \
            IF ACABOU THEN \
            LEAVE loop_com_atendimento; \
            END IF; \
            SELECT COUNT(*) INTO @vTEM FROM TB_ATENDIMENTO \
            WHERE DATA = pDATA_ATENDIMENTO \
            AND CPF_PROFISSIONAL = vCPF_AUX; \
            IF @vTEM <= 0 THEN \
                SET vCPF = vCPF_AUX; \
            END IF; \
        END LOOP loop_com_atendimento; \
    END IF; \
    CLOSE cPROFISSIONAL; \
    RETURN vCPF; \
end;"

    regra_2 = "create  function REGRA_2( \
pCADASTRO VARCHAR(200), \
pTIPO VARCHAR(200) \
) \
returns FLOAT(2) \
deterministic \
begin \
    declare vPRECO float(2); \
    SELECT COUNT(*) INTO @vCONT_ADOTADO FROM TB_ADOTA WHERE CADASTRO_PET = pCADASTRO; \
    SELECT COUNT(*) INTO @vCONT_ATENDIDO FROM TB_ATENDIMENTO WHERE CADASTRO_PET = pCADASTRO; \
    SELECT PRECO INTO @PRECINHO FROM TB_SERVICO WHERE TIPO_SERVICO = pTIPO; \
    SET vPRECO = @PRECINHO; \
    IF @vCONT_ADOTADO > 0 AND @vCONT_ATENDIDO <= 0 THEN \
        SET vPRECO = 0; \
    END IF; \
    IF vPRECO = 0 THEN \
        DELETE FROM TB_ADOTA WHERE CADASTRO_PET = pCADASTRO; \
    END IF;    \
    RETURN vPRECO; \
end;"

    regra_3 = "create  function REGRA_3( \
QUANTIDADE_GASTA  FLOAT \
) \
returns varchar(15) \
deterministic \
begin \
    declare vNIVEL varchar(15); \
    if 50 > QUANTIDADE_GASTA then \
        SET vNIVEL := 'Sem Nivel'; \
    elseif QUANTIDADE_GASTA >= 50 and QUANTIDADE_GASTA < 150 then  \
        SET vNIVEL := 'Filhote'; \
    elseif QUANTIDADE_GASTA >= 150 and QUANTIDADE_GASTA < 300 then \
        SET vNIVEL := 'Mascote'; \
    else \
        SET vNIVEL := 'Rei da Selva'; \
    end if; \
        return (vNIVEL); \
end;"
    connect = mysql.connector.connect(user='b39ac2ee88031a', password='029444b5',  
                                      host='us-cdbr-east-04.cleardb.com',
                                      database='heroku_204f5e4dda9919c')
    cursor = connect.cursor()
    cursor.execute(regra_1)
    cursor.execute(regra_2)
    cursor.execute(regra_3)
    
