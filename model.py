from sqlalchemy.ext.hybrid import hybrid_method
from jsabrandeis import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
        self.authenticated = False

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @hybrid_method
    def is_correct_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User {0}>'.format(self.email)

