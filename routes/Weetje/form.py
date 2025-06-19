from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional
from models import Behandeling

class WeetjeForm(FlaskForm):
    Weetje = StringField('Weetje', validators=[DataRequired()])
    uitleg = StringField('Uitleg', validators=[Optional()] )
    gender = SelectField('Waar-of-nietwaar', choices=[('waar', 'waar'), ('nietwaar', 'nietwaar')], validators=[DataRequired()])
    Behandeling_id = SelectField('Behandeling', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Opslaan')

    def __init__(self, *args, **kwargs):
        super(WeetjeForm, self).__init__(*args, **kwargs)
        self.Behandeling_id.choices = [(k.id, k.behandelingnaam) for k in Behandeling.query.all()]
