
from models.pet import PetModel
from models.profissional import ProfissionalModel
from models.servico import ServicoModel


def preenncher_banco():

	import pandas as pd
	import numpy as np
	from models.produto import ProdutoModel
	import datetime


	formato = '%d/%m/%Y'
	dados_produtoss = pd.read_excel('teste.xlsx', sheet_name=0)
	tabela_matriz_produtos = np.asarray(dados_produtoss)
	dados_pets = pd.read_excel('teste.xlsx', sheet_name=1)
	tabela_matriz_pets = np.asarray(dados_pets)
	dados_profissionais = pd.read_excel('teste.xlsx', sheet_name=2)
	tabela_matriz_profissionais = np.asarray(dados_profissionais)
	dados_servico = pd.read_excel('teste.xlsx', sheet_name=3)
	tabela_matriz_servico = np.asarray(dados_servico)


	lista_dados_produtos = []
	for linha in tabela_matriz_produtos:
		lista = []
		for i in range(0, len(linha)):
			if i == len(linha) - 2:
				lista.append(float(linha[i]))
			elif i == len(linha) - 1:
				lista.append(int(linha[i]))
			else:
				lista.append(str(linha[i]))
		lista_dados_produtos.append(lista)

	for linha in lista_dados_produtos:
		produto = ProdutoModel(*linha)
		produto.salvar_produto()

	date_time = None
	lista_dados_pets = []
	for linha in tabela_matriz_pets:
		lista = []
		for i in range(0, len(linha)):
			if i == len(linha) - 3:
				datetime_obj = datetime.datetime.strptime(str(linha[i]), formato)
				lista.append(datetime_obj.date())
			else:
				lista.append(str(linha[i]))
		lista_dados_pets.append(lista)
	
	for linha in lista_dados_pets:
		for i in range(0, len(linha)):
			if i == 2:
				date_time = linha[i]
				linha.remove(linha[i])
			
		pet = PetModel(*linha)
		pet.colocar_data_nascimento(date_time)
		pet.colocar_dono_do_pet(None)
		pet.salvar_pet()

	
	lista_dados_profissionais = []
	for linha in tabela_matriz_profissionais:
		lista = []
		for i in range(0, len(linha)):
			if i == len(linha) - 1:
				datetime_obj = datetime.datetime.strptime(str(linha[i]), formato)
				lista.append(datetime_obj.date())
			else:
				lista.append(str(linha[i]))
		lista_dados_profissionais.append(lista)
	
	for linha in lista_dados_profissionais:
		profissional = ProfissionalModel(*linha)
		profissional.salvar_profissional()

	
	listas_dados_servicos = []
	for linha in tabela_matriz_servico:
		lista = []
		for i in range(0, len(linha)):
			if i == len(linha) - 1:
				lista.append(float(linha[i]))
			else:
				lista.append(str(linha[i]))
		listas_dados_servicos.append(lista)
	
	for linha in listas_dados_servicos:
		servico = ServicoModel(*linha)
		servico.salvar_servico()

	



	





