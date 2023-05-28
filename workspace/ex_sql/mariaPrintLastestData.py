import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='mydb'
    )

cur = db.cursor()
cur.execute("select * from myTable order by time desc limit 1")

rows = cur.fetchall() #query -> rows(data) 

for row in rows:
    print(row)
    
db.close()