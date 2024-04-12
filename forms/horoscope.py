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
