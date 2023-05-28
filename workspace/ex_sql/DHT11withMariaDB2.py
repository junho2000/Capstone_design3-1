import pymysql
import board
import adafruit_dht

#initial the dht device, with data pin connected to: board.D6 -> GPIO 06, 
dhtDevice = adafruit_dht.DHT11(board.D6)
db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='mydb'
    )

cur = db.cursor()

temperature_c = dhtDevice.temperature
temperature_f = temperature_c * (9/5) + 32
humidity = dhtDevice.humidity
print(
    "Temp: {:.1f}F / {:.1f}C Humidity: {}%".format(
        temperature_f, temperature_c, humidity)
    )
if humidity is not None and temperature_c is not None:
    cur.execute('insert into myTable value(now(), {0}, {1})'.format(temperature_c/1, humidity/1))
else:
    print('Failed to get reading')

db.commit()

cur.execute('select * from myTable order by time desc limit 1')
row = cur.fetchall()
print(row)

db.close()