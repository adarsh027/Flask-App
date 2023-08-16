from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func

from flask_mysqldb import MySQL
 
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'mydb'
 
mysql = MySQL(app)


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },                      
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        result=cur.execute(f"SELECT * from users where email= '{email}'")
        if result:
            if check_password_hash(result.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('firstName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cur = mysql.connection.cursor()
        result=cur.execute(f"SELECT * from users where email= '{email}'")
        if result:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 7 characters.', category='error')
        else:
            password = generate_password_hash(password1, method='sha256')
            cur.execute(f"INSERT INTO users(first_name,last_name, email,password) VALUES('{first_name}', '{last_name}','{email}', '{password}')")
            mysql.connection.commit()
            cur.close()
            flash('Account created!', category='success')
            return redirect(url_for('home'))

    return render_template("register.html", user=current_user)


if __name__ == '__main__':
    app.run(debug=True)