# Autor: Wiiu Lopes
# Data: 10/10/2018
# Linguagem: Python

# ========= IMPORTANTE ===========
# O codigo esta livre para usar,
# citar e compartilhar desde que
# mantida sua fonte e seu autor.
# Obrigado.

#! /usr/bin/env python

import time
import os
import sys
import pymysql

#=========================================================================================================================
def conectaBanco():

	HOST = "localhost"
	USER = "root"
	PASSWD = "Wiiu12345*"
	BANCO = "vision"

	try:
		conecta = pymysql.connect(HOST, USER, PASSWD)
		conecta.select_db(BANCO)

    	except pymysql.Error, e:
        	print "Erro: O banco especificado nao foi encontrado...",e
		menu = raw_input()
		opcaoUsuario()

	return conecta

def funcCadastrar(conecta):
    print "\n\nDigite os dados:\n"
    pontoInteresse = str(raw_input("Nome Ponto Referencia: "))
    pontoInteresse = (pontoInteresse.upper())
    lat = float(raw_input("Latitude: "))
    lng = float(raw_input("Longitude: "))
    cursor = conecta.cursor()

    sql = "INSERT INTO coordenada (lat,lng,ponto_interesse) VALUES (lat,lng,'" + pontoInteresse + "')"

    try:
        cursor.execute(sql)
        conecta.commit()

    except pymysql.Error, e:
        print "Erro: " + sql
        print e

    print "Dados gravados com sucesso."
    conecta.close()
    menu = raw_input()
    opcaoUsuario()

def funcConsultar(conecta):

	name = str(raw_input("\nDigite o Ponto Interesse a Pesquisar: "))
	name = (name.upper())
	resultados = 0
	cursor = conecta.cursor()
	sql = ("SELECT * FROM coordenada WHERE ponto_interesse LIKE '%"+name+"%'")


	try:
		cursor.execute(sql)
		resultado = cursor.fetchall()

		for dados in resultado:
			ide = dados[0]
			lat = dados[1]
			lng = dados[2]
			ponto_interesse = dados[3]
			resultados = int(resultados)
			resultados = resultados + 1
			print"----------------------------------"
			print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s" % (
				ide, lat, lng, ponto_interesse)
		conecta.commit()

	except pymysql.Error, e:
		print "Erro: " + sql
		print e

	print "\n\nForam encontrados %d resultados" % resultados
	conecta.close()
	menu = raw_input()
	opcaoUsuario()

# =========================================================================================================================
def funcAlterar(conecta):
    print "\n\nDigite os dados:\n"
    ide = raw_input("ID do ponto de interesse a alterar: ")
    novo_nome = raw_input("Novo Nome do Ponto de Interesse: ")
    novo_nome = (novo_nome.upper())
    cursor = conecta.cursor()

    sql = "UPDATE coordenada SET ponto_interesse='" + novo_nome + "' WHERE id='" + ide + "'"
    try:
        cursor.execute(sql)
        conecta.commit()

    except pymysql.Error, e:
        print "Erro: " + sql
        print e

    print "Alteracao feita com sucesso."
    conecta.close()
    menu = raw_input()
    opcaoUsuario()

#=========================================================================================================================
def funcExcluir(conecta):

	print "\n\nDigite os dados:\n"
	ide_exclusao = raw_input("ID a Excluir: ")
	cursor = conecta.cursor()

	sql = "DELETE FROM coordenada WHERE id='"+ide_exclusao+"'"
	try:
        	cursor.execute(sql)
		conecta.commit()

    	except pymysql.Error, e:
        	print "Erro: " + sql
        	print e

	print "Exclusao feita com Sucesso."
	conecta.close()
	menu = raw_input()
	opcaoUsuario()

# =========================================================================================================================
def funcMostrarTodos(conecta):
	resultados = 0
	cursor = conecta.cursor()
	sql = "SELECT * FROM coordenada;"

	try:
		cursor.execute(sql)
		resultado = cursor.fetchall()

		for dados in resultado:
			ide = dados[0]
			lat = dados[1]
			lng = dados[2]
			ponto_interesse = dados[3]
			resultados = int(resultados)
			resultados = resultados + 1
			print"----------------------------------"
			print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s" % (
			ide, lat, lng, ponto_interesse)
		conecta.commit()

	except pymysql.Error, e:
		print "Erro: " + sql
		print e

	print "\n\nForam encontrados %d resultados" % resultados
	conecta.close()
	menu = raw_input()
	opcaoUsuario()

#=========================================================================================================================
def opcaoUsuario():
	print "==================================="
	print "======= Banco de Coordenadas ========"
	print "==================================="
	opcao = raw_input("Escolha a opcao desejada\n\n[1] - Cadastrar\n[2] - Consultar\n[3] - Alterar\n[4] - Excluir\n[5] - Mostrar Todos\n[6] - Sair")

	try:
		opcao = int(opcao)
		if opcao<1 or opcao>6:
			print "OPCAO INVALIDA: Verifique o valor digitado"
			time.sleep(2)
			opcaoUsuario()
	except:
		print "OPCAO INVALIDA: Verifique o valor digitado"
		time.sleep(2)
		opcaoUsuario()
	if opcao == 1:
		conecta = conectaBanco()
		funcCadastrar(conecta)

	elif opcao == 2:
		conecta = conectaBanco()
		funcConsultar(conecta)

	elif opcao == 3:
		conecta = conectaBanco()
		funcAlterar(conecta)

	elif opcao == 4:
		conecta = conectaBanco()
		funcExcluir(conecta)

	elif opcao == 5:
		conecta = conectaBanco()
		funcMostrarTodos(conecta)

	elif opcao == 6:
		sys.exit()

#=========================================================================================================================
if __name__=='__main__':
	opcaoUsuario()