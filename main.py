from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/start')  # фотографии с темами в два столбика
def start():
    return render_template("start.html")

'''def main():
    db_session.global_init("db/blogs.db")
    app.run()'''


if __name__ == '__main__':
    '''main()'''
    app.run(port=8080, host='127.0.0.1')
