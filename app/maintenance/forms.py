from flask_wtf import FlaskForm
from app import app
from wtforms import StringField, BooleanField,TextAreaField,SubmitField, validators,RadioField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField,DateField
from app.maintenance.models import getProperties


#form for maintenance related input
class MaintenanceForm(FlaskForm):
    #location is pulling from the database so it is dynamic
    location = SelectField('location',validators=[DataRequired()], choices = [(c['ID'], c['Address']) for c in getProperties()])
    description = TextAreaField('description',validators=[DataRequired()])
    dateofwork = DateField('dateofwork',format='%Y-%m-%d')

    #only used on data updated through a modal window.
    id = HiddenField('id')

    submit = SubmitField('Submit')
