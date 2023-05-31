import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='mydb'
    )

cur = db.cursor()
cur.execute("insert into myTable values (now(),1,2)")
db.commit()
cur.execute("select * from myTable")

rows = cur.fetchall() #query -> rows(data) 

for row in rows:
    print(row)
    
db.close()