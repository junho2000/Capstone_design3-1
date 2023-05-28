import pymysql

db = pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')

cur = db.cursor()
cur.execute("SELECT * FROM tblRegister") # usemySQL cursor
rows = cur.fetchall()
print(rows)
db.commit()
db.close()