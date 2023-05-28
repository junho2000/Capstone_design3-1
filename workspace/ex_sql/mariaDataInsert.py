import pymysql

db = pymysql.connect(host='localhost',user='root',password='1234',db='mydb')

cur = db.cursor()

sql = "insert into tblRegister values('rabbit','5678','kim','123456','1234567','panda@kookmin.ac.kr','010-222-2222','5678','77 Jeongneng-ro','Programmer');"

cur.execute(sql)

db.commit()
db.close()