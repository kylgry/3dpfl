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

class Printer(db.Model):

    __tablename__ = 'printers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'model': self.model,
        }

class Filament(db.Model):

    __tablename__ = 'filaments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
        }


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    printer_modified = db.Column(db.Boolean, nullable=False)
    printer_id = db.Column(db.ForeignKey('printers.id'), nullable=False)
    filament_id = db.Column(db.ForeignKey('filaments.id'), nullable=False)
    failure = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    user = db.relationship('User')
    printer = db.relationship('Printer')
    filament = db.relationship('Filament')
    comments = db.relationship('Comment')
    votes = db.relationship('Vote')


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.ForeignKey('posts.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user = db.relationship('User')


class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('users.id'))
    post_id = db.Column(db.ForeignKey('posts.id'))
    db.UniqueConstraint(user_id, post_id)
