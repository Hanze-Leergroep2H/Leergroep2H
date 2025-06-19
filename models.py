import enum
from flask_login import UserMixin
from extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(enum.Enum):
    USER = 'user'
    BEHEERDER = 'beheerder'
    ADMIN = 'admin'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(Role), nullable=True, default=Role.USER)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role.name}')"

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_beheerder(self):
        return self.role == Role.BEHEERDER

    def is_user(self):
        return self.role == Role.USER

class Beheerder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Behandeling = db.relationship('Behandeling', backref='Beheerder', lazy=True)

class Behandeling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    behandelingnaam = db.Column(db.String(50), nullable=False)
    Categorie = db.Column(db.String(10), nullable=False)
    Beheerder_id = db.Column(db.Integer, db.ForeignKey('beheerder.id'), nullable=False)
    Weetje = db.relationship('Weetje', backref='Behandeling', lazy=True)

class Weetje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Weetje = db.Column(db.String(50), nullable=False)
    uitleg = db.Column(db.String, nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    Behandeling_id = db.Column(db.Integer, db.ForeignKey('behandeling.id'), nullable=False)
