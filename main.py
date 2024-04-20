from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.horoscopes import Horoscope
from data.users import User
from forms.horoscope import Create
from forms.user import Register, Login

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
data = [['aries', 'Овен'], ['taurus', 'Телец'],
        ['gemini', 'Близнецы'], ['cancer', 'Рак'],
        ['leo', 'Лев'], ['virgo', 'Дева'],
        ['libra', 'Весы'], ['scorpio', 'Скорпион'],
        ['sagittarius', 'Стрелец'], ['capricorn', 'Козерог'],
        ['aquarius', 'Водолей'], ['pisces', 'Рыбы']]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")

        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    birthday=form.birthday.data)
        if form.email.data == 'daniilroitenberg@yandex.ru':
            user.redactor = True
        user.set_password(form.password.data)
        user.create_zodiac_sign(str(form.birthday.data))
        sess.add(user)
        sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['POST', 'GET'])
def index():
    global data
    if current_user.is_authenticated:
        sess = db_session.create_session()
        sign = current_user.zodiac_sign
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()

        with open(f'static/horoscopes_data/{sign}.txt', 'r', encoding='utf8') as file:
            lines = file.readlines()
            index = lines.index('\n')
            characteristic = ''.join(lines[:index])
            year_horoscope = ''.join(lines[index:])

        return render_template('index.html', sign=sign, route=f'static/img/{horoscope.image}',
                               day_horoscope=horoscope.day_horoscope, characteristic=characteristic,
                               year_horoscope=year_horoscope, data=data)

    return render_template('index.html')


@app.route('/<sign>', methods=['POST', 'GET'])
def show_sign(sign):
    if current_user.is_authenticated:
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()

        with open(f'static/horoscopes_data/{sign}.txt', 'r', encoding='utf8') as file:
            lines = file.readlines()
            index = lines.index('\n')
            characteristic = ''.join(lines[:index])
            year_horoscope = ''.join(lines[index:])

        return render_template('index.html', sign=sign, route=f'static/img/{horoscope.image}',
                               day_horoscope=horoscope.day_horoscope, characteristic=characteristic,
                               year_horoscope=year_horoscope, data=data)


@app.route('/info', methods=['POST', 'GET'])
def info():
    return render_template('info.html')


@app.route('/create', methods=['POST', 'GET'])
def create_horoscope():
    form = Create()
    if form.validate_on_submit():
        with open(f'static/horoscopes_data/{form.sign.data}.txt', 'w', encoding='utf8') as file:
            file.write(form.characteristic.data)
            file.write('\n\n')
            file.write(form.year_horoscope.data)
        sess = db_session.create_session()
        horoscope = Horoscope(sign=form.sign.data,
                              image=form.image.data,
                              day_horoscope=form.day_horoscope.data,
                              data=f'{form.sign.data}.txt')
        sess.merge(horoscope)
        sess.commit()

        return redirect('/')
    return render_template('create_horoscope.html', form=form)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    return 'not yet'


def main():
    db_session.global_init('db/horoscopes.db')
    app.run()


if __name__ == '__main__':
    main()
