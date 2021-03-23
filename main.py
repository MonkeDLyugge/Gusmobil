from data import db_session
from data.users import Users
from data.ads import Ads
from data.favorites import Favorites
from forms.login import LoginForm
from forms.ads import Adds
from forms.register import RegisterForm
from flask import Flask, request, abort
from flask import render_template, redirect
from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ISBN5-89392-055-4'


def main():
    db_session.global_init('db/gus_auto.db')
    app.run()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_ad', methods=['GET', 'POST'])
def add_ads():
    form = Adds()
    if form.validate_on_submit():
        session = db_session.create_session()
        add = Adds(
            brand=form.brand.data,
            model=form.model.data,
            price=form.price.data,
            transmission=form.transmission.data,
            engine=form.engine.data,
            steering_wheel=form.steering_wheel.data,
            power=form.power.data,
            drive_unit=form.drive_unit.data,
            mileage=form.mileage.data,
            year=form.year.data,
            about=form.about.data
            )
        session.add(add)
        session.commit()
        return redirect('/')
    return render_template('add_ad.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def entrance():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.is_remember_me.data)
            return redirect("/")
        return render_template('entrance.html',
                               message='Неверный логин или пароль!',
                               form=form)
    return render_template('entrance.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(Users).filter(Users.email == form.email.data).first():
            return render_template("register.html", title="Регистрация", form=form,
                                   message="Такой пользователь уже есть")
        user = Users(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
