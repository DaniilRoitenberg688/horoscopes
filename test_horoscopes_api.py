from requests import get

print(get('http://localhost:5000/api/horoscopes').json())
print()
print(get('http://localhost:5000/api/horoscopes/leo').json())