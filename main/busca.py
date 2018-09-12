import pymysql
conn= pymysql.connect(host='localhost',port=3306, user='root',password='Wiiu12345*',db='vision')
cur = conn.cursor()
cur.execute("SELECT * FROM coordenada")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()