from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_restful import Api

from data import db_session, news_api, news_resources
from data.cosmo_news import Cosmo_News
from data.earth_news import Earth_News
from data.day_news import Day_News
from data.new_year_news import New_Year_News
from data.users import User
from forms.comments import NewsForm
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/cosmoexample')
def cosmo():
    db_sess = db_session.create_session()
    cosmo_news = db_sess.query(Cosmo_News)
    return render_template('cosmoexample.html', news=cosmo_news)


@app.route('/earthexample')
def earth():
    db_sess = db_session.create_session()
    news = db_sess.query(Earth_News)
    return render_template('earthexample.html', news=news)


@app.route('/oneexample')
def one():
    db_sess = db_session.create_session()
    news = db_sess.query(Day_News)
    return render_template('oneexample.html', news=news)


@app.route('/yearexample')
def year():
    db_sess = db_session.create_session()
    news = db_sess.query(New_Year_News)
    return render_template('yearexample.html', news=news)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/cosmoexample/comment',  methods=['GET', 'POST'])
@login_required
def add_cosmo_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Cosmo_News()
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/cosmoexample')
    return render_template('comment.html', title='Добавление комментария',
                           form=form)


@app.route('/earthexample/comment',  methods=['GET', 'POST'])
@login_required
def add_earth_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Earth_News()
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/earthexample')
    return render_template('comment.html', title='Добавление комментария',
                           form=form)


@app.route('/oneexample/comment',  methods=['GET', 'POST'])
@login_required
def add_day_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Day_News()
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/oneexample')
    return render_template('comment.html', title='Добавление комментария',
                           form=form)


@app.route('/yearexample/comment',  methods=['GET', 'POST'])
@login_required
def add_new_year_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = New_Year_News()
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/yearexample')
    return render_template('comment.html', title='Добавление комментария',
                           form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    # для списка объектов
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    # для одного объекта
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
    app.run()


if __name__ == '__main__':
    main()
