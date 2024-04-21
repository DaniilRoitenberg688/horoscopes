from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Create(FlaskForm):
    sign = StringField('Sign name', validators=[DataRequired()])
    image = StringField('Image route', validators=[DataRequired()])
    day_horoscope = TextAreaField('Day horoscope', validators=[DataRequired()])
    characteristic = TextAreaField('Characteristic', validators=[DataRequired()])
    year_horoscope = TextAreaField('Year horoscope', validators=[DataRequired()])
    submit = SubmitField('CREATE', validators=[DataRequired()])


class EditAll(FlaskForm):
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
    sign = StringField('Sign name', validators=[DataRequired()])
    day_horoscope = TextAreaField('Day horoscope', validators=[DataRequired()])
    submit = SubmitField('EDIT', validators=[DataRequired()])