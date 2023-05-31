import requests
import json

city = "Seoul"
apiKey = "2c7e42c78013055d71893c31f9577c7a"
lang = 'kr'
units = 'metric'
api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"

result = requests.get(api)
result = json.loads(result.text)

name = result['name']
lon = result['coord']['lon']
lat = result['coord']['lat']
weather = result['weather'][0]['main']
temperature = result['main']['temp']
humidity = result['main']['humidity']
pressure = result['main']['pressure']
visibility = result['visibility']
windspeed = result['wind']['speed']
winddirection = result['wind']['deg']
clouds = result['clouds']['all']
sunrise = result['sys']['sunrise']
sunset = result['sys']['sunset']

print(f'city: {name} (longitude = {lon}, latitude = {lat})')
print(f'=======================================================')
print(f'weather = {weather}')
print(f'temperature = {temperature} C')
print(f'humidity = {humidity} %')
print(f'air pressure = {pressure} hPa')
print(f'wind speed = {windspeed} m/s')
print(f'cloudiness = {clouds}')