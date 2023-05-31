import requests
import json

city = "Seoul"
apiKey = "2c7e42c78013055d71893c31f9577c7a"
lang = 'kr'
units = 'metric'
api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"

result = requests.get(api)
result = json.loads(result.text)

print(result)