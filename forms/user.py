from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    """Форма регистрации"""

    # имя
    name = StringField('Ваше имя', validators=[DataRequired()])

    # фамилия
    surname = StringField('Ваша фамилия', validators=[DataRequired()])

    # почта
    email = EmailField('Почта', validators=[DataRequired()])

    # день рождения
    birthday = DateField('Дата рождения', validators=[DataRequired()])

    # пароль
    password = PasswordField('Пароль', validators=[DataRequired()])

    # пароль еще раз
    password_again = PasswordField('Пароль еще раз', validators=[DataRequired()])

    # кнопка подтверждения
    submit = SubmitField('Зарегистрироваться')


class Login(FlaskForm):
    """Форма входа"""

    # почта
    email = EmailField('Почта', validators=[DataRequired()])

    # пароль
    password = PasswordField('Пароль', validators=[DataRequired()])

    # галочка запомни меня
    remember_me = BooleanField('Запомнить меня')

    # кнопка подтверждения
    submit = SubmitField('Войти')


