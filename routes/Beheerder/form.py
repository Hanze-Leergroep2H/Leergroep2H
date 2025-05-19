from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class BeheerderForm(FlaskForm):
    naam = StringField('naam', validators=[DataRequired()])
    gender = SelectField('gender', choices=[('Vrouw', 'Vrouw'), ('Man', 'Man'), ('Onzijdig', 'Onzijdig')], validators=[DataRequired()])
    submit = SubmitField('Opslaan')

    def __init__(self, *args, **kwargs):
        super(BeheerderForm, self).__init__(*args, **kwargs)
