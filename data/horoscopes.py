import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Horoscope(SqlAlchemyBase, SerializerMixin):
    """Модель гороскопа"""
    __tablename__ = 'horoscopes'
    # айди
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # название знака
    sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # файл с картинкой
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # ежедневный гороскоп
    day_horoscope = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # файл с характеристикой знака зодиака и с годовым гороскопом
    data = sqlalchemy.Column(sqlalchemy.String, nullable=True)
