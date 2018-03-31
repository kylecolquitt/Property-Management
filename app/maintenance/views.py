from app import app
from flask import render_template, redirect,url_for,session,Blueprint,request, flash
from app.maintenance.forms import MaintenanceForm
from app.maintenance.models import Maintenance
from app.admin.models import Content, sendAdminEmail, sendUserEmail
import html
mtn = Blueprint('mtn', __name__, url_prefix='/maintenance')

@mtn.before_request
def begin():
    #if user is not logged in and user is not a tenant or admin, send back to home page with alert message
    if session.get('logged_in') == True and session.get('role') == 1 or session.get('role')==3:
        None
    else:
        flash('You are not authorized to access this page','danger')
        return redirect(url_for('home.index'))

@mtn.route('/maintenance-request', methods=['POST', 'GET'])
def form():
    form = MaintenanceForm()
    maintenance = Maintenance()
    
    #load content from database to be displayed in right nav on maintenance
    #request form page.
    content = Content()
    content = content.getContentById('maintenance')
    
    #if form is submitted
    if request.method=='POST':
        #add form information to database
        main = maintenance.addRequest(form)
        sendAdminEmail('maintenanceAdmin',form)
        sendUserEmail('maintenanceTenant',form)

        #return to home page with message.

        flash('Your Maintenance Request has been recieved','info')
        return redirect(url_for('home.index'))
    
    #load maintenance form page with content to be loaded. The content is html escaped so convert
    #back to regular html using unescape. Also pass the maintenacne form to the template.
    return render_template('maintenance/maintenance-form.html',form=form, content=html.unescape(content[2]))

