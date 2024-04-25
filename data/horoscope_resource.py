from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.horoscopes_reqparse import parser, parser_for_edit_one
from data.horoscopes import Horoscope


def abort_if_horoscope_not_found(sign):
    sess = db_session.create_session()
    job = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
    if not job:
        abort(404, message='Horoscope not found')


class HoroscopeResource(Resource):
    def get(self, sign):
        abort_if_horoscope_not_found(sign)
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
        return jsonify({'horoscope': horoscope.to_dict(only=('sign', 'image', 'day_horoscope', 'data'))})

    def delete(self, sign):
        abort_if_horoscope_not_found(sign)
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()
        sess.delete(horoscope)
        sess.commit()
        return jsonify({'result': 'OK'})

class HoroscopeListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        horoscopes = sess.query(Horoscope).all()
        return jsonify({'horoscopes': [horoscope.to_dict(only=('sign', 'image', 'day_horoscope', 'data')) for horoscope
                                       in horoscopes]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        new_horoscope = Horoscope(sign=args['sign'],
                                  image=args['image'],
                                  day_horoscope=args['day_horoscope'],
                                  data=args['data'])

        sess.merge(new_horoscope)
        sess.commit()
        return jsonify({'result': 'OK'})




