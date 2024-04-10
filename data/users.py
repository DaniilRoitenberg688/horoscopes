import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    birthday = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    redactor = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    zodiac_sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def create_zodiac_sign(self, date: str):
        _, month, day = date.split('-')

        day, month = int(day), int(month)
        if month == 3 and day >= 21 or month == 4 and day <= 19:
            self.zodiac_sign = 'aries'
        elif month == 4 and day >= 20 or month == 5 and day <= 20:
            self.zodiac_sign = 'taurus'
        elif month == 5 and day >= 21 or month == 6 and day <= 21:
            self.zodiac_sign = 'gemini'
        elif month == 6 and day >= 22 or month == 7 and day <= 22:
            self.zodiac_sign = 'cancer'
        elif month == 7 and day >= 23 or month == 8 and day <= 22:
            self.zodiac_sign = 'leo'
        elif month == 8 and day >= 23 or month == 9 and day <= 22:
            self.zodiac_sign = 'virgo'
        elif month == 9 and day >= 23 or month == 10 and day <= 22:
            self.zodiac_sign = 'libra'
        elif month == 10 and day >= 23 or month == 11 and day <= 21:
            self.zodiac_sign = 'scorpio'
        elif month == 11 and day >= 22 or month == 12 and day <= 21:
            self.zodiac_sign = 'sagittarius'
        elif month == 12 and day >= 22 or month == 1 and day <= 19:
            self.zodiac_sign = 'capricorn'
        elif month == 1 and day >= 20 or month == 2 and day <= 18:
            self.zodiac_sign = 'aquarius'
        elif month == 2 and day >= 19 or month == 3 and day <= 20:
            self.zodiac_sign = 'pisces'
