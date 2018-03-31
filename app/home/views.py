from app import app,DB
import pymysql
from flask import render_template, redirect,url_for,session,Blueprint
from app.admin.models import Content
import html
home = Blueprint('home', __name__, url_prefix='/')

@home.route('/')
def index():
    error = None
    content = Content()
    #load home page content from database.
    content=content.getContentById('home')
    
    return render_template('home/home.html', error=error, content=html.unescape(content[2]))

@home.route('<error>')
def indexerror(error):
    return render_template('home/home.html', error=error)

