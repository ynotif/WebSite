import re
from flask import Flask, render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Ключ
    login = db.Column(db.String(64), nullable=False)  # Длина строки максимальная + не может быть пустым
    password = db.Column(db.String(128), nullable=False)
    password2 = db.Column(db.String(128), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']
        if not is_valid_email(login):
            return 'Некорректный почтовый адрес!'
        if User.query.filter_by(login=login).first():
            return "Такой логин уже существует"  # Сделать чтобы возвращало "Такой логин уже существует"
        elif password == password2 and 10 > len(password) > 0:
            user = User(login=login, password=password, password2=password2)
            # Сделай крч возвращение ошибки с фронта если чет не так
        else:
            return render_template('register.html')
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        except:
            return 'Error'
    else:
        return render_template('register.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=login, password=password).first()
        if user:
            return redirect('/')
        else:
            return "Error"
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)  # сменить потом на false
