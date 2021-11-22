
def preenncher_banco():

    import pandas as pd
    import numpy as np
    from models.produto import ProdutoModel


    dados = pd.read_excel('teste.xlsx')
    tabela_matriz = np.asarray(dados)


    lista_dados = []
    for linha in tabela_matriz:
        lista = []
        for i in range(0, len(linha)):
            if i == len(linha) - 2:
                lista.append(float(linha[i]))
            elif i == len(linha) - 1:
                lista.append(int(linha[i]))
            else:
                lista.append(str(linha[i]))
        lista_dados.append(lista)

    for linha in lista_dados:
        produto = ProdutoModel(*linha)
        try:
            produto.salvar_produto()
        except:
            print('nao salvou')



