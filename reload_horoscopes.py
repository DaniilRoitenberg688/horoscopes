from bs4 import BeautifulSoup
from requests import get

from data.db_session import create_session
from data.horoscopes import Horoscope



def reload():

    sess = create_session()

    all_horoscopes = sess.query(Horoscope).all()

    for i in all_horoscopes:
        answer = get(f'https://horo.mail.ru/prediction/{i.sign}/today/').text

        html = BeautifulSoup(answer, 'html.parser')
        text = html.find(class_='article__item').text
        i.day_horoscope = text
        sess.commit()


if __name__ == '__main__':
    reload()
