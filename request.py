import requests

url = 'http://localhost:9696/predict'  


datapoint = {
    "soil_type": "slightly acidic",
    "humidity": 40,
    "phosphorus_level": 12.7,
    "soil_moisture": 14.4,
    "nitrogen_level": 45.5
}

response = requests.post(url, json=datapoint)
result = response.json()

print('response:', result)