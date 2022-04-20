from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password):

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class PrinterBrand(db.Model):

    __tablename__ = 'printerbrands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.Text, nullable=False)

class Printer(db.Model):

    __tablename__ = 'printers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.ForeignKey('printerbrands.id'))
    model = db.Column(db.Text, nullable=False)

class FilamentBrand(db.Model):

    __tablename__ = 'filamentbrands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.Text, nullable=False)

class Filament(db.Model):

    __tablename__ = 'filaments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.ForeignKey('filamentbrands.id'), nullable=False)
    type = db.Column(db.Text, nullable=False)


class FailureCategory(db.Model):

    __tablename__ = 'failurecategories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.ForeignKey('failurecategories.id'), nullable=False)
    printer = db.Column(db.ForeignKey('printers.id'), nullable=False)
    filament = db.Column(db.ForeignKey('filaments.id'), nullable=False)
    failure = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)

class Vote(db.Model):

    __tablename__ = 'votes'

    username = db.Column(db.ForeignKey('users.id'), primary_key=True)
    post = db.Column(db.ForeignKey('posts.id'), primary_key=True)
