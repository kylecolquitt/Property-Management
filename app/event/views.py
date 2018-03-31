from app import app
from flask import render_template, redirect,url_for,session,Blueprint, request, flash
from app.event.models import Event
from app.event.forms import EventForm
from app.admin.models import Content, sendAdminEmail,sendUserEmail
import html
event = Blueprint('event', __name__, url_prefix='/event')

@event.before_request
def begin():
    #if user is  not logged in, redirect to login page
    if session.get('logged_in') == True:
        None
    else:
        return redirect(url_for('auth.login'))


@event.route('/event-request', methods=['GET','POST'])
def form():
    form = EventForm()
    event = Event()

    #load content from db to be displayed on the event request form page
    content = Content()
    content = content.getContentById('private')
    
    # if form is submitted
    if request.method == 'POST':

        #add event request to database
        event.addRequest(form)

        #send admin an email to notify of request.
        sendAdminEmail('eventAdmin',form)
        
        #send user an email to notify of their request.
        sendUserEmail('eventCustomer',form)
        flash('Your Private event Request has been recieved', 'info')
        # redirect to home page with message
        return redirect(url_for('home.index'))
    
    # load event request form with the content to be loaded and the form. Unescape the escaped html
    return render_template('event/event-form.html',form=form,content=html.unescape(content[2]))

