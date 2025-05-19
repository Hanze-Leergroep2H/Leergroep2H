from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

from models import Beheerder

class BehandelingForm(FlaskForm):
    behandelingnaam = StringField('behandelingnaam', validators=[DataRequired()])
    Categorie = SelectField(
        'Categorie behandeling',
        choices=[
            ('Radiologie', 'Radiologie'),
            ('Cardiologie', 'Cardiologie'),
            ('levertransplantatie', 'levertransplantatie')
        ],
        validators=[DataRequired()]
    )
    Beheerder_id = SelectField(
        'Beheerder',
        coerce=lambda x: int(x) if x and x != 'None' else None,
        validators=[Optional()] 
    )
    submit = SubmitField('Opslaan')

    def __init__(self, *args, **kwargs):
        super(BehandelingForm, self).__init__(*args, **kwargs)
        self.Beheerder_id.choices = [('', '--- Geen Beheerder geselecteerd ---')] + [
            (k.id, k.naam) for k in Beheerder.query.all()
        ]
