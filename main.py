from flask import Flask, render_template, redirect
from flask_login import LoginManager

from data import db_session
from data.users import User
from forms.user import Register

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
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

        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/horoscopes.db')
    app.run()


if __name__ == '__main__':
    main()
