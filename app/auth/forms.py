from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,TextAreaField,SubmitField, validators,RadioField,SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

STATE_ABBREV = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')

class AdminForm(FlaskForm):
    first_name = StringField('first_name',validators=[DataRequired()])
    last_name = StringField('last_name',validators=[DataRequired()])
    email = EmailField('email',validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')

class RegisterForm(FlaskForm):
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
    password = PasswordField('password')