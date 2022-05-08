from flask import Flask, request, jsonify, render_template, abort, session, flash, redirect
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Printer, Filament, Post, Comment, Vote
from forms import RegisterForm, LoginForm, PostForm
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

    return render_template('root.html')


@app.route('/register')
def show_register():

    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/register', methods=["POST"])
def handle_register():

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

@app.route('/posts')
def show_posts():

    printer = request.args.get('printer')
    filament = request.args.get('filament')

    if printer == '':
        printer = None;

    if filament == '':
        filament = None;

    if printer == None and filament == None:
        posts = Post.query.all()
    elif filament == None:
        posts = db.session.query(Post).filter(Post.printer.has(model=printer)).all()
    elif printer == None:
        posts = db.session.query(Post).filter(Post.filament.has(type=filament)).all()
    else:
        posts = db.session.query(Post).filter(Post.printer.has(model=printer)).filter(Post.filament.has(type=filament)).all()

    filter = {'printer': printer,'filament': filament }

    return render_template('posts.html', posts=posts, filter=filter)

@app.route('/posts/<id>')
def show_post(id):

    post = Post.query.get(id)
    return render_template('post.html', post=post)

@app.route('/posts/new')
def show_add_post():

    if not 'user_id' in session:
        flash("You must login first to post")
        return redirect("/")

    form = PostForm()
    form.printer_modified.choices = [(1, "Stock"),(2, "Modified")]
    return render_template('postnew.html', form=form)

@app.route('/posts/new', methods=["POST"])
def add_post():

    if not 'user_id' in session:
        flash("You must login first to post")
        return redirect("/")

    form = PostForm()
    form.printer_modified.choices = [(1, "Stock"),(2, "Modified")]

    user = User.query.get(session["user_id"])

    if form.validate_on_submit():

        failure = form.failure.data
        solution = form.solution.data

        if form.printer_modified.data == 1:
            printer_modified = False
        else:
            printer_modified = True

        if form.printer.data not in [r for (r,) in db.session.query(Printer.model)]:
            printer = Printer(model=form.printer.data)
            db.session.add(printer)
            db.session.commit()
        else:
            printer = db.session.query(Printer).filter_by(model=form.printer.data).first()

        if form.filament.data not in [r for (r,) in db.session.query(Filament.type)]:
            filament = Filament(type=form.filament.data)
            db.session.add(filament)
            db.session.commit()
        else:
            filament = db.session.query(Filament).filter_by(type=form.filament.data).first()

        post = Post(user_id=user.id, printer_modified=printer_modified, printer_id=printer.id, filament_id=filament.id, failure=failure, solution=solution)
        db.session.add(post)
        db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/_list/<table>/<column>')
def get_list(table,column):

    models = {  "printer": Printer,
                "filament": Filament }

    list = [r for (r,) in db.session.query(getattr(models[table],column)).all()]

    return jsonify(list=list)
