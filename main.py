from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api

from data import db_session
from data.horoscope_resource import HoroscopeListResource, HoroscopeResource
from data.horoscopes import Horoscope
from data.user_resource import UserResource, UserListResource
from data.users import User
from forms.horoscope import Create, EditAll, EditOne
from forms.user import Register, Login

# создаем и настраиваем приложение
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# создаем апи
api = Api(app, catch_all_404s=True)

# список со всеми знаками зодиака на русском и английском
sign_names = [['aries', 'Овен'], ['taurus', 'Телец'],
              ['gemini', 'Близнецы'], ['cancer', 'Рак'],
              ['leo', 'Лев'], ['virgo', 'Дева'],
              ['libra', 'Весы'], ['scorpio', 'Скорпион'],
              ['sagittarius', 'Стрелец'], ['capricorn', 'Козерог'],
              ['aquarius', 'Водолей'], ['pisces', 'Рыбы']]


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница с регистрацией"""
    # создаем форму
    form = Register()

    # проверяем нажатие кнопки
    if form.validate_on_submit():

        # проверяем совпадают ли пароль, если нет, то говорим об этом
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")

        # проверяем есть ли аккаунт у этого пользователя, если есть то сообщаем об этом
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")

        # если все нормально, то создаем нового пользователя и направляем его на страницу для входа
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    birthday=form.birthday.data)
        if form.email.data == 'daniilroitenberg@yandex.ru':
            user.redactor = True
        user.set_password(form.password.data)
        print(form.birthday.data)
        user.create_zodiac_sign(str(form.birthday.data))
        sess.add(user)
        sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в аккаунт"""

    # создаем форму
    form = Login()

    # проверяем нажатие кнопки
    if form.validate_on_submit():

        # если такой пользователь есть и введен верный пароль, то перенаправляем его на основную страницу,
        # если нет, то сообщаем об этом
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
    """Выход из аккаунта"""
    logout_user()
    return redirect("/")


@app.route('/', methods=['POST', 'GET'])
def index():
    """Главная страница"""
    global sign_names
    # если пользователь вошел в свой аккаунт показываем его данные и гороскопы
    if current_user.is_authenticated:
        sess = db_session.create_session()
        sign = current_user.zodiac_sign

        # находим данные гороскопа в соответствии с его знаком зодиака
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()

        # открываем файл с характеристикой знака зодиака и гороскопом на год
        with open(f'static/horoscopes_data/{sign}.txt', 'r', encoding='utf8') as file:
            lines = file.readlines()
            index = lines.index('\n')
            characteristic = ''.join(lines[:index])
            year_horoscope = ''.join(lines[index:])

        for g, i in sign_names:
            if sign == g:
                sign = i

        # возвращаем шаблон передавая туда все необходимое
        return render_template('index.html', sign=sign, route=f'static/img/{horoscope.image}',
                               day_horoscope=horoscope.day_horoscope, characteristic=characteristic,
                               year_horoscope=year_horoscope, data=sign_names, title='Гороскопы', is_footer=True)

    return render_template('index.html', title='Гороскопы')


@app.route('/<sign>', methods=['POST', 'GET'])
def show_sign(sign):
    """Страница с определенным знаком зодиака (на нее можно перейти кликнув на знак зодиака в футере)"""

    # проверяем залогинин ли пользователь
    if current_user.is_authenticated:
        sess = db_session.create_session()
        horoscope = sess.query(Horoscope).filter(Horoscope.sign == sign).first()

        # берем русское название знака зодиака
        rus_sign = ''
        for i, g in sign_names:
            if i == sign:
                rus_sign = g

        # берем все годовой гороскоп и характеристику знака зодиака
        with open(f'static/horoscopes_data/{sign}.txt', 'r', encoding='utf8') as file:
            lines = file.readlines()
            index = lines.index('\n')
            characteristic = ''.join(lines[:index])
            year_horoscope = ''.join(lines[index:])

        for g, i in sign_names:
            if sign == g:
                sign = i

        # возвращаем шаблон со всеми необходимыми данными
        return render_template('index.html', sign=sign, route=f'static/img/{horoscope.image}',
                               day_horoscope=horoscope.day_horoscope, characteristic=characteristic,
                               year_horoscope=year_horoscope, data=sign_names, title=rus_sign, is_footer=True)


@app.route('/info', methods=['POST', 'GET'])
def info():
    """Страничка с информацией о сайте"""
    return render_template('info.html', title='Информация')


@app.route('/create', methods=['POST', 'GET'])
def create_horoscope():
    """Страничка для создания гороскопа"""
    # создаем форму
    form = Create()

    # проверяем нажата ли кнопка
    if form.validate_on_submit():
        # записываем данные годового гороскопа и характеристики знака зодиака в файл
        with open(f'static/horoscopes_data/{form.sign.data}.txt', 'w', encoding='utf8') as file:
            file.write(form.characteristic.data)
            file.write('\n\n')
            file.write(form.year_horoscope.data)

        # добавляем новый гороскоп в бд
        sess = db_session.create_session()
        horoscope = Horoscope(sign=form.sign.data,
                              image=form.image.data,
                              day_horoscope=form.day_horoscope.data,
                              data=f'{form.sign.data}.txt')
        sess.merge(horoscope)
        sess.commit()

        return redirect('/')
    return render_template('create_horoscope.html', form=form, title='Создание')


@app.route('/edit_all', methods=['POST', 'GET'])
def edit_all():
    """Страница для редактирования всех дневных гороскопов сразу"""

    # создаем форму
    form = EditAll()

    # проверяем нажатие кнопки
    if form.validate_on_submit():

        # пробегаемся по всем знакам зодиака в таблице и меням дневной гороскоп
        sess = db_session.create_session()
        all_horoscopes = sess.query(Horoscope)
        for horoscope in all_horoscopes:
            sign = horoscope.sign
            horoscope.day_horoscope = form.data[sign]
            sess.commit()
        return redirect('/')
    return render_template('edit_all.html', form=form, title="Редактировать все")


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    """Страница для редактирования одного гороскопа"""

    # создаем форму
    form = EditOne()

    # проверяем нажатие кнопки
    if form.validate_on_submit():

        # проверяем есть ли название гороскопа, который был введен в нашей бд, если да то меням дневной гороскоп,
        # если нет сообщаем об этом
        sess = db_session.create_session()
        all_names = [i[0] for i in sess.query(Horoscope.sign)]
        if form.sign.data not in all_names:
            return render_template('edit_one.html', form=form, message='No such sign')

        zodiac_sign = sess.query(Horoscope).filter(Horoscope.sign == form.sign.data).first()
        zodiac_sign.day_horoscope = form.day_horoscope.data
        sess.commit()
        return redirect('/')
    return render_template('edit_one.html', form=form, title='Редактировать один')


def main():
    # подключаемся к бд
    db_session.global_init('db/horoscopes.db')

    # подключаем апи гороскопов
    api.add_resource(HoroscopeResource, '/api/horoscopes/<sign>')
    api.add_resource(HoroscopeListResource, '/api/horoscopes/')

    # подключаем апи пользователя
    api.add_resource(UserResource, '/api/users/<id>')
    api.add_resource(UserListResource, '/api/users/')

    # запускаем приложение
    app.run('127.0.0.1', 5000)


if __name__ == '__main__':
    main()
