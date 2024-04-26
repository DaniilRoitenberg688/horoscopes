from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.horoscopes import Horoscope
from data.horoscopes_reqparse import parser


def abort_if_horoscope_not_found(sign):
    """Проверка существует ли гороскоп, который мы ищем"""
    sess = db_session.create_session()
    horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
    if not horoscope:
        abort(404, message='Horoscope not found')


class HoroscopeResource(Resource):
    """Ресурс для одного гороскопа"""

    def get(self, sign):
        """Возвращаем информацию о знаке зодиака"""
        abort_if_horoscope_not_found(sign)
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
        return jsonify({'horoscope': horoscope.to_dict(only=('sign', 'image', 'day_horoscope', 'data'))})

    def delete(self, sign):
        """Удаляем знак зодиака"""
        abort_if_horoscope_not_found(sign)
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
        sess.delete(horoscope)
        sess.commit()
        return jsonify({'result': 'OK'})


class HoroscopeListResource(Resource):
    """Ресурс для группы гороскопов"""

    def get(self):
        """Возвращаем информацию обо всех знаках зодиака"""
        sess = db_session.create_session()
        horoscopes = sess.query(Horoscope).all()
        return jsonify({'horoscopes': [horoscope.to_dict(only=('sign', 'image', 'day_horoscope', 'data')) for horoscope
                                       in horoscopes]})

    def post(self):
        """Создаем новый знак зодиака"""
        args = parser.parse_args()
        sess = db_session.create_session()
        new_horoscope = Horoscope(sign=args['sign'],
                                  image=args['image'],
                                  day_horoscope=args['day_horoscope'],
                                  data=args['data'])

        sess.merge(new_horoscope)
        sess.commit()
        return jsonify({'result': 'OK'})
