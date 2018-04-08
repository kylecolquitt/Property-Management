import os
from flask import Flask
from flask_ckeditor import CKEditor
from flask_mail import Mail
from config import ADMINS, SECRET_KEY, DB, MAIL_USERNAME, BASE_MAIL_LINK
from flask_oauthlib.client import OAuth
from flask_bcrypt import Bcrypt
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['DB'] = DB
bcrypt = Bcrypt(app)
app.config.from_object('config')
mail = Mail(app)


from app.google.views import goog
from app.home.views import home
from app.event.views import event
from app.maintenance.views import mtn
from app.auth.views import auth
from app.admin.views import admin
app.register_blueprint(goog)
app.register_blueprint(home)
app.register_blueprint(event)
app.register_blueprint(mtn)
app.register_blueprint(auth)
app.register_blueprint(admin)










