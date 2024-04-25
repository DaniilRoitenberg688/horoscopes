from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Create(FlaskForm):
    """Форма для создания гороскопа"""

    # знак
    sign = StringField('Sign name', validators=[DataRequired()])

    # имя картинки
    image = StringField('Image route', validators=[DataRequired()])

    # гороскоп на сегодня
    day_horoscope = TextAreaField('Day horoscope', validators=[DataRequired()])

    # характеристика знака зодиака
    characteristic = TextAreaField('Characteristic', validators=[DataRequired()])

    # гороскоп на год
    year_horoscope = TextAreaField('Year horoscope', validators=[DataRequired()])

    # кнопка подтверждения
    submit = SubmitField('CREATE', validators=[DataRequired()])


class EditAll(FlaskForm):
    """Форма для редактирования всех гороскопов разом"""

    aries = TextAreaField('Овен', validators=[DataRequired()])
    taurus = TextAreaField('Телец', validators=[DataRequired()])
    gemini = TextAreaField('Близнецы', validators=[DataRequired()])
    cancer = TextAreaField('Рак', validators=[DataRequired()])
    leo = TextAreaField('Лев', validators=[DataRequired()])
    virgo = TextAreaField('Дева', validators=[DataRequired()])
    libra = TextAreaField('Весы', validators=[DataRequired()])
    scorpio = TextAreaField('Скорпион', validators=[DataRequired()])
    sagittarius = TextAreaField('Стрелец', validators=[DataRequired()])
    capricorn = TextAreaField('Козерог', validators=[DataRequired()])
    aquarius = TextAreaField('Водолей', validators=[DataRequired()])
    pisces = TextAreaField('Рыбы', validators=[DataRequired()])
    submit = SubmitField('EDIT', validators=[DataRequired()])


class EditOne(FlaskForm):
    """Форма для редактирования одного гороскопа"""
    # название знака зодиака
    sign = StringField('Sign name', validators=[DataRequired()])

    # данные гороскопа
    day_horoscope = TextAreaField('Day horoscope', validators=[DataRequired()])

    # кнопка подтверждения
    submit = SubmitField('EDIT', validators=[DataRequired()])