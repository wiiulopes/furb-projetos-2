# Autor: Wiiu Lopes
# Data: 04/10/2018
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
import string
import MySQLdb

#=========================================================================================================================
def conectaBanco():

    HOST = "localhost"
    PORT = 3306
    USER = "root"
    PASSWD = "Wiiu12345*"
    BANCO = "vision"

	try:
		conecta = MySQLdb.connect(HOST,PORT, USER, PASSWD)
		conecta.select_db(BANCO)

    except MySQLdb.Error, e:
        	print "Erro: O banco especificado nao foi encontrado...",e
		menu = raw_input()
		os.system("clear")
		opcaoUsuario()
return conecta

# =========================================================================================================================
def funcCadastrar(conecta):
    print "\n\nDigite os dados:\n"
    pontoInteresse = str(raw_input("Nome Ponto Referencia: "))
    pontoInteresse = (pontoInteresse.upper())
    lat = str(raw_input("Latitude: "))
    lat = (lat.upper())
    lng = str(raw_input("Longitude: "))
    lng = (lng.upper())
    cursor = conecta.cursor()

    sql = "INSERT INTO coordenada (lat,lng,pontoInteresse) VALUES ('" + lat + "','" + lng + "','" + pontoInteresse + "')"

    try:
        cursor.execute(sql)
        conecta.commit()

    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e

    print "Dados gravados com sucesso."
    conecta.close()
    menu = raw_input()
    os.system("clear")
    opcaoUsuario()

#=========================================================================================================================

def funcConsultar(conecta):

	busca = str(raw_input("\nDigite o Ponto Interesse a Pesquisar: "))
	busca = (busca.upper())
	cursor = conecta.cursor()
 	sql=("SELECT * FROM coordenada WHERE ponto_interesse LIKE  '%%s%'  LIMIT 1", (busca,))

 	resultados = 0

   	try:
        	cursor.execute(sql)
		resultado = cursor.fetchall()
		for dados in resultado:
			ide = dados[0]
            latitude = dados[1]
			longitude = dados[2]
		    pontoInteresse = dados[3]
			resultados= int(resultados)
			resultados = resultados + 1
			print"\n----------------------------\n"
			print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s"%(
            ide, latitude, longitude, pontoInteresse)
		conecta.commit()

    	except MySQLdb.Error, e:
        	print "Erro: " + sql
        	print e

	print "\n\nForam encontrados %d resultados"%resultados
	conecta.close()
	menu = raw_input()
	os.system("clear")
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

    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e

    print "Alteracao feita com sucesso."
    conecta.close()
    menu = raw_input()
    os.system("clear")
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

    	except MySQLdb.Error, e:
        	print "Erro: " + sql
        	print e

	print "Exclusao feita com Sucesso."
	conecta.close()
	menu = raw_input()
	os.system("clear")
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
            latitude = dados[1]
            longitude = dados[2]
            pontoInteresse = dados[3]
            resultados = int(resultados)
            resultados = resultados + 1
            print"----------------------------------"
            print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s" % (
            ide, latitude, longitude, pontoInteresse)
        conecta.commit()

    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e

    print "\n\nForam encontrados %d resultados" % resultados
    conecta.close()
    menu = raw_input()
    os.system("clear")
    opcaoUsuario()

#=========================================================================================================================
def opcaoUsuario():

	os.system("clear");
	print "==================================="
	print "======= Ponto de Interesse ========"
	print "==================================="
	opcao = raw_input("Escolha a opcao desejada\n\n[1] - Cadastrar\n[2] - Consultar\n[3] - Alterar\n[4] - Excluir\n[5] - Mostrar Todos\n[6] - Sair")

	try:
		opcao = int(opcao)
		if opcao<1 or opcao>6:
			os.system("clear");
			print "OPCAO INVALIDA: Verifique o valor digitado"
			time.sleep(2)
			opcaoUsuario()
	except:
		os.system("clear");
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
