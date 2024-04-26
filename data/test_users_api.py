from requests import post, get, delete

# создаем тестового пользователя
print(post('http://localhost:5000/api/users/',
           json={'name': 'test', 'surname': 'test', 'email': 'test@m.ru', 'password': '1', 'sign': 'cancer',
                 'redactor': 0}).json())
print()

# выводим его
print(get('http://localhost:5000/api/users/15').json())
print()

# удаляем его
print(delete('http://localhost:5000/api/users/15').json())
print()

# выводим всех пользователей
print(get('http://localhost:5000/api/users/').json())
