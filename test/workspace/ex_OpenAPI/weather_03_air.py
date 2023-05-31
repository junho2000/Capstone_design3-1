import requests
import json

city = "Seoul"
apiKey = "2c7e42c78013055d71893c31f9577c7a"
lon = 126.9778
lat = 37.5683
lang = 'kr'
api = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apiKey}"

result = requests.get(api)
result = json.loads(result.text)

lon = result['coord']['lon']
lat = result['coord']['lat']
aqi = result['list'][0]['main']['aqi']
co = result['list'][0]['components']['co']
no = result['list'][0]['components']['no']
no2 = result['list'][0]['components']['no2']
o3 = result['list'][0]['components']['o3']
so2 = result['list'][0]['components']['so2']
pm2_5 = result['list'][0]['components']['pm2_5']
pm10 = result['list'][0]['components']['pm10']
nh3 = result['list'][0]['components']['nh3']

print(f'longitude = {lon}, latitude = {lat}')
print(f'=======================================================')
print(f'air quality index = {aqi}')
print(f'PM2.5 index = {pm2_5}')
print(f'PM10 index = {pm10}')
