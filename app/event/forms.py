from flask_wtf import FlaskForm
from app import app
from wtforms import StringField, BooleanField,TextAreaField,SubmitField, validators,RadioField,SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField, DateField
from app.maintenance.models import getProperties
from app.event.models import getEventType

class EventForm(FlaskForm):
    # this field is dynamically pulling event types from the database
    event_type = SelectField('event_type',validators=[DataRequired()], choices = [(c['ID'], c['Type']) for c in getEventType()])
    #this field is dynamically pulling properties from the database
    location = SelectField('location',validators=[DataRequired()], choices = [(c['ID'], c['Address']) for c in getProperties()])
    description = TextAreaField('description',validators=[DataRequired()])
    eventdate = DateField('eventdate',format='%Y-%m-%d')

    # only used for editing event in modal window
    id = HiddenField('id')

    receipt = StringField('receipt')
    invoice = StringField('invoice')

    submit = SubmitField('Submit')