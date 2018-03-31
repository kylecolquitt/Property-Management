import os
from flask import Flask
from flask_ckeditor import CKEditor
from flask_mail import Mail
from config import ADMINS, SECRET_KEY, DB, MAIL_USERNAME, BASE_MAIL_LINK
from flask_oauthlib.client import OAuth
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['DB'] = DB
bcrypt = Bcrypt(app)
app.config.from_object('config')
mail = Mail(app)
oauth = OAuth(app)
ckeditor = CKEditor(app)




# Import a module / component using its blueprint handler variable
from app.auth.views import auth
from app.home.views import home
from app.event.views import event
from app.maintenance.views import mtn
from app.admin.views import admin


# Register blueprint(s)
app.register_blueprint(mtn)
app.register_blueprint(event)
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(admin)
