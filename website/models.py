from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()

db = SQLAlchemy()


@login_manager.user_loader
def load_user(user_id):
    return Gebruiker.query.get(user_id)

class Gebruiker(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    wachtwoord_hash = db.Column(db.String(128))

    def __init__(self, username: str, email: str, wachtwoord: str):
        self.username = username
        self.email = email
        self.set_wachtwoord(wachtwoord)

    def set_wachtwoord(self, wachtwoord):
        self.wachtwoord_hash = bcrypt.generate_password_hash(wachtwoord).decode('utf-8')

    def check_wachtwoord(self, wachtwoord):
        return bcrypt.check_password_hash(self.wachtwoord_hash, wachtwoord)

class Behandeling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    behandelingnaam = db.Column(db.String(50), nullable=False)
    Categorie = db.Column(db.String(10), nullable=False)
    Weetje = db.relationship('Weetje', backref='Behandeling', lazy=True)

class Weetje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Weetje = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Behandeling_id = db.Column(db.Integer, db.ForeignKey('Behandeling.id'), nullable=False)
