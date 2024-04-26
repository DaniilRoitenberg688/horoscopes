from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.users import User
from data.users_reqparse import parser


def abort_if_user_not_found(id):
    """Проверяем существует ли пользователь"""
    sess = db_session.create_session()
    user = sess.query(User).get(id)
    if not user:
        abort(404, message='User not found')


class UserResource(Resource):
    """Ресурс для одного пользователя"""

    def get(self, id):
        """Возвращаем одного пользователя"""
        abort_if_user_not_found(id)
        sess = db_session.create_session()
        user = sess.query(User).get(id)
        return jsonify({'user': user.to_dict(only=('name', 'email', 'birthday', 'zodiac_sign'))})

    def delete(self, id):
        """Удаляем пользователя"""
        abort_if_user_not_found(id)
        sess = db_session.create_session()
        user = sess.query(User).get(id)
        sess.delete(user)
        sess.commit()
        return jsonify({'result': 'OK'})


class UserListResource(Resource):
    """Ресурс для группы пользователей"""

    def get(self):
        """Возвращаем всех пользователей"""
        sess = db_session.create_session()
        users = sess.query(User).all()
        return jsonify({'users': [user.to_dict(only=('name', 'email', 'birthday', 'zodiac_sign')) for user in users]})

    def post(self):
        """Создаем пользователя"""
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(name=args['name'],
                    surname=args['surname'],
                    email=args['email'],
                    zodiac_sign=args['sign'])
        user.set_password(args['password'])

        sess.merge(user)
        sess.commit()
        return jsonify({'result': 'OK'})
