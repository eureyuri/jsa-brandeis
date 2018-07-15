from sqlalchemy.ext.hybrid import hybrid_method
from jsabrandeis import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    # TODO: Hash
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
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
        return self.password == password

    @property
    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return '<User {0}>'.format(self.name)

