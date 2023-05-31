import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='1234',
                     db='mydb')
cur = db.cursor()

cur.execute("SELECT * FROM myStudents")
rows = cur.fetchall() # Stored as tuples

print(f'The first entity is {rows[0]}.')
print(f'The second entity is {rows[1]}.')

print(f'\nThe third entity is ID={rows[2][0]}, ', end='')
print(f'math={rows[2][1]}, english={rows[2][2]}, science={rows[2][3]}.')

math_sum = 0
english_sum = 0
science_sum = 0

print('\nPrint all the entities in the table.')
for row in rows:
    print(row)

for row in rows:
    math_sum += row[1]
    english_sum += row[2]
    science_sum += row[3]
    
math_avg = math_sum / len(rows)
english_avg = english_sum / len(rows)
science_avg = science_sum / len(rows)

print(f'\nThere are {len(rows)} entities in the table.')
print(f'[Averages] math = {math_avg}, ', end='')
print(f'english = {english_avg}, science = {science_avg}')

personal_average1 = (rows[0][1]+rows[0][2]+rows[0][3]) / 3
print(f'\nThe personal average score of ID = {rows[0][0]} is {personal_average1:.2f}.')

db.commit()
db.close()
