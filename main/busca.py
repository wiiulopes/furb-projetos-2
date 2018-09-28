from pymysql import connect, Error


#Busca todos pontos de interesse
def select_all_coordenada():
    try:
        conn = connect(host='localhost', port=3306, user='root', password='Wiiu12345*', db='vision')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenada")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

#Busca pontos de interesse conforme filtro
def select_lat_lng():
    try:
        conn = connect(host='localhost', port=3306, user='root', password='Wiiu12345*', db='vision')
        cursor = conn.cursor()
        q = "SELECT * FROM coordenada where lat = %(value)s and lng = %(value2)s"
        params = {'value': '-26.91534000', 'value2': '-49.08198400'}
        cursor.execute(q, params)

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    select_all_coordenada()
    select_lat_lng()