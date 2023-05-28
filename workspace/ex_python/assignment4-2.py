import pymysql

db = pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')

cur = db.cursor()
sql = "insert into tblRegister values('hallo', '4233', 'kim', '123456', '123456', 'panda@kookmin.ac.kr', '010-222-2222', '5678', '77-jeongneng-ro','player');"

cur.execute(sql)

db.commit()

db.close()