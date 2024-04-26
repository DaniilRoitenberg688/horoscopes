from requests import post, get, delete

# создаем тестовый гороскоп
print(post('http://localhost:5000/api/horoscopes/',
           json={'sign': 'test', 'image': 'test', 'day_horoscope': 'test', 'data': 'test'}).json())
print()

# выводим его
print(get('http://localhost:5000/api/horoscopes/test').json())
print()

# удаляем его
print(delete('http://localhost:5000/api/horoscopes/test').json())
print()

# выводим все гороскопы
print(get('http://localhost:5000/api/horoscopes/').json())
