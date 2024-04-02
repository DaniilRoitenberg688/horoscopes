from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    surname = StringField('Your surname', validators=[DataRequired()])
    email = EmailField('Your email', validators=[DataRequired()])
    birthday = DateField('Yor birthday', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired()])
    password_again = PasswordField('Again', validators=[DataRequired()])
    submit = SubmitField('REGISTER')
