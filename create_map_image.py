import requests

response = 'https://static-maps.yandex.ru/1.x/?ll=37.287388,55.568807&z=16&l=map&pt=37.287388,55.568807,comma'

answer = requests.get(response)

with open('static/img/map.png', 'wb') as file:
    file.write(answer.content)