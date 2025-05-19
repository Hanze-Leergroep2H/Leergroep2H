from flask import Blueprint, render_template, url_for, flash, redirect
from extensions import db, bcrypt
from .forms import RegistrationForm, LoginForm
from models import User
from flask_login import login_user, current_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Je account is aangemaakt! Je kunt nu inloggen.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('auth.user'))
        else:
            flash('Inloggen mislukt. Controleer je email en wachtwoord.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route("/user")
@login_required
def user():
    return render_template('auth/user.html', title='Account')
