from flask import Flask, request, jsonify, render_template, abort, session, flash, redirect
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Printer, FilamentBrand, Filament, FailureCategory, Post, Comment, Vote
from forms import RegisterForm, LoginForm
from keys import FLASK_SECRET_KEY
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///3dpfl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

connect_db(app)

# from flask_debugtoolbar import DebugToolbarExtension
# debug = DebugToolbarExtension(app)

def login(user):

    session["user_id"] = user.id


def logout():

    if "user_id" in session:
        del session["user_id"]
        flash("logout successful")


@app.route('/')
def show_root():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():


    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(username=form.username.data, password=form.password.data)
            db.session.commit()

        except IntegrityError:
            flash("registration error")
            return render_template('register.html', form=form)

        login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)


@app.route('/login')
def show_login():

    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/login', methods=["POST"])
def handle_login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login(user)
            flash("login successful")
            return redirect("/")

        flash("invalid username or password")

    return render_template('login.html', form=form)

@app.route('/logout')
def handle_logout():

    logout()

    return redirect('/')

# @app.route('/post')
# def show_post():
