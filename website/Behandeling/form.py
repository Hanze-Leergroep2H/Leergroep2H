from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class BehandelingForm(FlaskForm):
    behandelingnaam = StringField('behandelingnaam', validators=[DataRequired()])
    Categorie = SelectField('Categorie', choices=[('Radiologie', 'Radiologie'), ('Cardiologie', 'Cardiologie'), ('levertransplantatie', 'levertransplantatie')], validators=[DataRequired()])
    submit = SubmitField('Opslaan')
