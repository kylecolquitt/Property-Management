from app import app,bcrypt,mail, MAIL_USERNAME, BASE_MAIL_LINK
from flask import render_template, redirect, g, \
                url_for, request,session,escape,flash, url_for, Blueprint, flash
from app.auth.models import User
from app.auth.forms import LoginForm, RegisterForm
import urllib.parse as urlparse
from datetime import timedelta
from flask_mail import Message
from uuid import uuid4
from app.admin.models import Content
import html


import re

auth = Blueprint('auth', __name__, url_prefix='/auth')

from flask import Flask, redirect, url_for, session, request, jsonify
import json


import httplib2


@auth.route('/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    user=User()

    #if form has been submitted
    if request.method=='POST':
        try:
            #check the person credentials against database
            person = user.checkLogin(form)
        except:
            #if for some reason the password doesn't exist. this should never be called. 
            flash('Password does not exist. Please use forgot password link to create a password')
            return render_template('login.html',form=form)

        if person:
            
            #if the credentials were correct, set session variables to track user information when logged in
            session['logged_in'] = True
            session['name'] = person[1] + ' ' + person[2]
            session['email'] = person[8]
            session['person_id'] = person[0]
            #add user role so the system knows what tabs and what to allow user access to.
            session['role'] = person[11]
            flash('Welcome!','success')
            return redirect(url_for('home.index'))
        else:

            #if the credentials were invalid
            flash('Invalid Login')


    #load login page with flask form
    return render_template('login.html',form=form)


@auth.route('/register', methods=['POST','GET'])
def register():
    form=RegisterForm()
    user=User()

    #if the form has been submitted
    if request.method=='POST':
        # check if the email entered exists, if true return to register page
        if user.checkEmail(form.email.data):
            flash('Email Exists. Please login or click Forgot Password if you forgot your password')

            return redirect(url_for('auth.register'))

        #else, add user to the database and send to login screen
        user.addUser(form)
        flash('Thanks for registering!', 'info')

        return redirect(url_for('auth.login'))

    #load the register page with form
    return render_template('register.html',form=form)


@auth.route('/forgot-password',methods=['POST','GET'])
def forgotPassword():
    form=LoginForm()
    user=User()

    #generate unique token
    rand_token = uuid4()

    #if email is submitted
    if request.method=='POST':

        #get user that has the submitted email
        person = user.getUser(form)

        #if person exists
        if person != None:
            user.deleteToken(person[0])
            #add token and url to database with personid
            user.addToken(person[0], str(rand_token))

            # get content to be sent in the forgot password email. The content is configurable.
            # the link is not configurable
            email = Content()
            x=email.getContentById('password')

            # send url with token in an email for user to access the password page
            # create url with the person id and random generated token.
            link = BASE_MAIL_LINK + "/auth/reset-password/"+str(person[0])+'/'+str(rand_token)
            msg = Message(x[3],
                  sender=MAIL_USERNAME,
                  recipients=[person[8]])
            msg.body=render_template('email/email.html',link=link, email=html.unescape(x[2]))
            msg.html=render_template('email/email.html',link=link, email=html.unescape(x[2]))
            mail.send(msg)
            #return to login page
            return redirect(url_for('auth.login'))  
    
    #return the forgot-password page for user to enter their email. 
    return render_template('forgot-password.html',form=form)


#this page is not accessible if the token has expired or does not exist in the database
@auth.route('/reset-password/<int:person_id>/<string:token>',methods=['POST','GET'])
def resetPassword(person_id, token):
    
    user=User()

    # this page can only be accessed if the token and person id in url matches the info in the forgot_password table

    #check the token and id
    if user.checkToken(person_id, token):
        
        #if correct, load password reset form
        form=LoginForm()

        #if form is submitted
        if request.method=='POST':

            #update the password column
            user.updatePassword(person_id,form.password.data)
            return redirect(url_for('auth.login'))

        return render_template('password-reset.html',form=form)
    else:

        #if token does not match, send back to login screen
        flash('Invalid Token!')
        return redirect(url_for('auth.login'))   
    return 'Failure'
    
  



@auth.route('/logout')
def logout():
    # clear session variables that track the user being logged in
    session.clear()
    for key in session.keys():
        session.pop(key)
    return redirect(url_for('home.index'))


