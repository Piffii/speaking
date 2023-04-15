from flask import Flask, render_template, json

app = Flask(__name__)


@app.route('/')
@app.route('/start')
def atsrt():
    return render_template("start.html")


@app.route('/registration')
def registration():
    return render_template("registration.html")


@app.route('/entrance')
def entrance():
    return render_template("entrance.html")


@app.route('/cosmoexample')
def cosmoexample():
    return render_template("cosmoexample.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
