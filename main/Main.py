# ! /usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Wiiu Lopes
# Data: 10/10/2018
# Linguagem: Python

# ========= IMPORTANTE ===========
# O codigo esta livre para usar,
# citar e compartilhar desde que
# mantida sua fonte e seu autor.
# Obrigado.

import time
import sys
import pymysql
import pyttsx
import math
import decimal
# =========================================================================================================================
def conectaBanco():
    HOST = "localhost"
    USER = "root"
    PASSWD = "Wiiu12345*"
    BANCO = "vision"

    try:
        conecta = pymysql.connect(HOST, USER, PASSWD)
        conecta.select_db(BANCO)

    except pymysql.Error, e:
        print "Erro: O banco especificado nao foi encontrado...", e
        menu = raw_input()
        opcaoUsuario()

    return conecta


def funcCadastrar(conecta):
    print "\n\nDigite os dados:\n"
    pontoInteresse = str(raw_input("Nome Ponto Interesse: "))
    pontoInteresse = (pontoInteresse.upper())
    lat = float(raw_input("Latitude: "))
    lng = float(raw_input("Longitude: "))
    cursor = conecta.cursor()

    try:
        cursor.execute("""INSERT INTO coordenada (lat,lng,ponto_interesse) VALUES (%s, %s, %s)""",
                       (lat, lng, pontoInteresse))
        conecta.commit()

    except pymysql.Error, e:
        print "Erro: " + cursor
        print e

    print "Dados gravados com sucesso."
    conecta.close()
    menu = raw_input()
    opcaoUsuario()


def funcConsultar(conecta):
    name = str(raw_input("\nDigite o nome do Ponto Interesse a Pesquisar: "))
    name = (name.upper())
    resultados = 0
    cursor = conecta.cursor()
    sql = ("SELECT * FROM coordenada WHERE ponto_interesse LIKE '%" + name + "%'")

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


# =========================================================================================================================
def funcExcluir(conecta):
    print "\n\nDigite os dados:\n"
    ide_exclusao = raw_input("ID a Excluir: ")
    cursor = conecta.cursor()

    sql = "DELETE FROM coordenada WHERE id='" + ide_exclusao + "'"
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


def funcSimulacao(conecta):
    en = pyttsx.init()
    en.setProperty('voice', b'brazil')
    en.setProperty('rate', 200)
    raio = 0.07
    resultados = 0
    idCount = 1
    cursor = conecta.cursor()

    cursor.execute("SELECT COUNT(*) FROM posicao_atual")
    resultadoCount = cursor.fetchone()[0]

    while idCount <= resultadoCount:
        cursor.execute("SELECT * FROM posicao_atual WHERE id='" + str(idCount)+"'")
        resultadosPosicaoAtual = cursor.fetchall()
        for dadosP in resultadosPosicaoAtual:
            lat = dadosP[1]
            lng = dadosP[2]

        print "\n\nPosição atual: Latitude " + str(lat) + " Logitude " + str(lng)

        pointA = lat, lng
        print "\n\nBuscando pontos de interesse no raio de " + str(raio * 1000) + " metros.\n"

        sql = ("SELECT *, (6371 * acos(cos(radians(" + str(lat) + ")) * cos(radians(lat)) * cos(radians(" + str(
            lng) + ")- radians(lng)) + sin(radians(" + str(
            lat) + ")) * sin(radians(lat))))AS distance FROM coordenada HAVING distance <= " + str(raio) + "")

        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if not resultado:
                print("Nenhum ponto de interesse no raio de "+ str(raio * 1000) + " metros.\n")
                time.sleep(3)

            for dados in resultado:
                ide = dados[0]
                lat = dados[1]
                lng = dados[2]
                ponto_interesse = dados[3]
                distance = round(dados[4], 4)
                distMetros = str(int(distance * 1000))
                pointB = lat,lng
                opcao = calculate_initial_compass_bearing(pointA, pointB)
                if distance >= 0.0005 and distance <= raio:
                    if opcao >= 0.0 and opcao <= 90.0:
                        direcao = "direita a frente"

                    elif opcao  >= 91.0 and opcao <= 180.0:
                        direcao = "direita atras"

                    elif opcao >= 181.0 and opcao <= 270.0:
                        direcao = "esquerda a tras"

                    elif opcao >=  271.0 and opcao <= 360.0:
                        direcao = "esquerda a frente"

                    en.say(ponto_interesse + " a " + distMetros + " metros " + direcao)
                    en.runAndWait()
                    print"------------------------------"
                    print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s\n Distancia: %s" % (
                            ide, lat, lng, ponto_interesse, distMetros + " metros " + direcao)
            conecta.commit()

        except pymysql.Error, e:
            print "Erro: " + sql
            print e


        idCount+=1

    conecta.close
    menu = raw_input()
    opcaoUsuario()

def funcCoordenada(conecta):
    en = pyttsx.init()
    en.setProperty('voice', b'brazil')
    en.setProperty('rate', 200)
    print "\n\nDigite os dados:\n"
    raioInit = float(raw_input("Informe o tamanho do raio em metros: "))
    raio = raioInit/1000
    lat = float(raw_input("Latitude: "))
    lng = float(raw_input("Longitude: "))

    resultados = 0
    cursor = conecta.cursor()
    sql = ("SELECT *, (6371 * acos(cos(radians(" + str(lat) + ")) * cos(radians(lat)) * cos(radians(" + str(
        lng) + ")- radians(lng)) + sin(radians(" + str(
        lat) + ")) * sin(radians(lat))))AS distance FROM coordenada HAVING distance <= " + str(raio) + "")

    try:
        cursor.execute(sql)
        resultado = cursor.fetchall()

        for dados in resultado:
            ide = dados[0]
            lat = dados[1]
            lng = dados[2]
            ponto_interesse = dados[3]
            distance = round(dados[4], 4)
            distMetros = str(int(distance * 1000))
            if distance >= 0.0005 and distance <= raio:
                en.say(ponto_interesse + " a " + distMetros + " metros")
                en.runAndWait()
                print"------------------------------"
                print " ID: %s\n Latitude: %s\n Longitude: %s\n Ponto de Interesse: %s\n Distancia: %s" % (
                        ide, lat, lng, ponto_interesse, distMetros + " metros")
        conecta.commit()

    except pymysql.Error, e:
        print "Erro: " + sql
        print e

    print "\n\nForam encontrados %d resultados" % resultados
    conecta.close
    menu = raw_input()
    opcaoUsuario()

def calculate_initial_compass_bearing(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# =========================================================================================================================
def opcaoUsuario():
    print "==================================="
    print "======= Black Glasses ========"
    print "==================================="
    opcao = raw_input(
        "Escolha a opcao desejada\n\n[1] - Cadastrar\n[2] - Consultar\n[3] - Alterar\n[4] - Excluir\n[5] - Mostrar Todos\n[6] - Consulta Ponto Interesse no Raio \n[7] - Simulacão\n[8] - Sair\n")

    try:
        opcao = int(opcao)
        if opcao < 1 or opcao > 8:
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
        conecta = conectaBanco()
        funcCoordenada(conecta)

    elif opcao == 7:
        conecta = conectaBanco()
        funcSimulacao(conecta)

    elif opcao == 8:
        sys.exit()


# =========================================================================================================================
if __name__ == '__main__':
    opcaoUsuario()
