from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,TextAreaField,SubmitField, validators,RadioField,SelectField,IntegerField, HiddenField,TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from app.admin.models import getCustomerType
from flask_ckeditor import CKEditorField


STATE_ABBREV = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')


class PersonForm(FlaskForm):
    first_name = StringField('first_name',validators=[DataRequired()])
    last_name = StringField('last_name',validators=[DataRequired()])
    email = EmailField('email',validators=[DataRequired()])
    organization = StringField('organization',validators=[DataRequired()])
    address = StringField('address',validators=[DataRequired()])
    city = StringField('city',validators=[DataRequired()])
    state = SelectField(label='State', choices=[(state, state) for state in STATE_ABBREV],default='UT')    
    zip = IntegerField('zip',validators=[DataRequired()])
    phone = IntegerField('phone',validators=[DataRequired()])
    ext = IntegerField('ext',validators=[DataRequired()])
    custtype = SelectField('custtype',validators=[DataRequired()], choices = [ (c['ID'], c['Type']) for c in getCustomerType()])

class AdminForm(FlaskForm):
    first_name = StringField('first_name',validators=[DataRequired()])
    last_name = StringField('last_name',validators=[DataRequired()])
    email = EmailField('email',validators=[DataRequired()])
    submit = SubmitField('Save')

class EmailForm(FlaskForm):
    email=EmailField('email')
    submit = SubmitField('Save')
    
class PropertyForm(FlaskForm):
    address = StringField('address',validators=[DataRequired()])
    description = StringField('description',validators=[DataRequired()])
    city = StringField('city',validators=[DataRequired()])
    state = StringField('state',validators=[DataRequired()])
    zip = StringField('zip',validators=[DataRequired()])
    p_type = SelectField('p_type',validators=[DataRequired()], choices=[('Commerical', 'Commerical'), ('Residential', 'Residential')])
    submit = SubmitField('Save')


class ContentForm(FlaskForm):
    key = HiddenField('key')
    subject = StringField('subject',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])
    submit = SubmitField('Save')
