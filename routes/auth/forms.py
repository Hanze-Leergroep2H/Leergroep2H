from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from models import User, Role

class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    confirm_password = PasswordField('Bevestig Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registreer')

    # Only shown to admin users
    role = SelectField('Rol', choices=[(role.value, role.name.title()) for role in Role], default='user')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Deze gebruikersnaam is al bezet.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Deze email is al geregistreerd.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow admins to see/change the role field
        if not current_user.is_authenticated or not current_user.is_admin():
            del self.role


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Login')
