from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

from models import Beheerder

# TODO when a beheerder creates a behandeling. dan moet de huidige user als beheerder worden teoegeveogd ipv dat je er uit moet kiezen.
# remove select option: replace with current_user.id

class BehandelingForm(FlaskForm):
    behandelingnaam = StringField('behandelingnaam', validators=[DataRequired()])
    Categorie = SelectField(
        'Categorie behandeling',
        choices=[
            ('Algemeen', 'Algemeen'),
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
