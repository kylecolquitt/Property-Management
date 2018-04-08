from app import app
from flask import render_template, redirect,url_for,session,Blueprint,request, flash
from app.maintenance.forms import MaintenanceForm
from app.event.forms import EventForm
from app.admin.forms import AdminForm, PropertyForm, PersonForm, ContentForm, EmailForm
from app.admin.models import Admin, Property, getCustomerTypeBId, Content
from app.maintenance.models import Maintenance
from app.event.models import Event
import datetime
import html,json
import requests

admin = Blueprint('admin', __name__, url_prefix='/administration')


@admin.before_request
def begin():
    #make sure user is logged in and has an admin role in the system.
    if 'credentials' not in session:
        return redirect('/google/authorize')
    if session.get('logged_in') == True and session.get('role') == 3:
        None
    else:
        flash('You are not authorized to access this page','danger')
        return redirect(url_for('home.index'))

##################################################
############### MANAGE ADMIN PAGES ###############
##################################################


@admin.route('/manageAdmin', methods=['GET','POST'])
def admins():
    admin = Admin()

    #load form for default email recipients table in template
    form = EmailForm()
    if request.method=='POST':
        admin.addEmail(form)

    #load the administrators template with the form, table of admins, and table of the default email recipients
    return render_template('administration/manage-administrators.html', form=form, admin=admin.getAdmins(), email = admin.getDefaultEmails())



@admin.route('/manageCustomers', methods=['GET','POST'])
def customers():
    admin = Admin()
    form = AdminForm()

    return render_template('administration/manage-customers.html', form=form, admin=admin.getCustomers())



@admin.route('/editPerson<int:person_id>', methods=['GET','POST'])
def editPerson(person_id):
    #edit a persons information . The person id is passed throught the url
    admin = Admin()
    form = PersonForm()

    if request.method=='POST':

        admin.updatePerson(form, person_id)
        return redirect(url_for('admin.admins'))
    else:
        #when the page is loaded, populate the form fields with current data
         admin.setPersonForm(form,person_id)

    #load person form with the users current customer/role type in the system.
    return render_template('administration/editPerson.html', form=form, customer_type = getCustomerTypeBId(person_id) )



@admin.route('/deleteEmail/<int:id>', methods=['GET','POST'])
def deleteAdmin(id):
    #delete a email from the default_recipients
    admin = Admin()
    admin.deleteEmail(id)

    return redirect(url_for('admin.admins'))

@admin.route('/maintenance',methods=['GET','POST'])
def maintenance():
    main = Maintenance()
    form=MaintenanceForm()
    x = None
    if request.method=='POST':

        #if the request is scheduled, add the scheduled date to the DB
        x=main.scheduleRequest(form)
        return render_template('administration/maintenance-requests.html', request=main.getRequest(0), form=form, completed=main.getRequest(1),x=json.dumps(x))

        #load the mainteance template with table of current requests,
        # schedule form that pops up in a modal, and table of complete/archive requests
    return render_template('administration/maintenance-requests.html', request=main.getRequest(0), form=form, completed=main.getRequest(1),x=json.dumps(x))

@admin.route('/maintenance/complete/<int:maintenance_id>/<int:complete>', methods=['GET', 'POST'])
def completeMaintenance(maintenance_id, complete):

    main = Maintenance()

    # mark a maintenance request complete. Url passes the id and the completeon status to be set for a request
    #this route handles marking and unmarking requests complete
    main.markComplete(maintenance_id, complete)
    return redirect(url_for('admin.maintenance'))

@admin.route('/event', methods=['GET','POST'])
def event():
    event = Event()
    form = EventForm()
    x = None
    if request.method=='POST':

        #add the invoice number, receipt number, and event date for a specific request.
        x = event.addInvRec(form)
        form =None
        form = EventForm()
        return render_template('administration/event-request.html',form=form, request = event.getRequest(), past=event.getPastEvents(), x=json.dumps(x))
    #load the event table template, with the form that is in a modal, the current requests table
    #and the past events table
    return render_template('administration/event-request.html',form=form, request = event.getRequest(), past=event.getPastEvents(),x=json.dumps(x))

@admin.route('/calendar')
def calendar():
    return render_template('administration/calendar.html')

#############################################
############### PROPERTY PAGES ##############
#############################################

@admin.route('/properties', methods=['GET','POST'])
def properties():
    form = PropertyForm()
    prop = Property()
    if request.method=='POST':

        #add a new property to the database
        prop.addProperty(form)

    return render_template('administration/properties.html', form=form, prop = prop.getProperties(0), archived = prop.getProperties(1))



@admin.route('/editProperty<int:property_id>', methods=['GET','POST'])
def editProperty(property_id):
    prop = Property()
    form = PropertyForm()
    if request.method=='POST':
        prop.updateProperty(form, property_id)
        return redirect(url_for('admin.properties'))
    else:
        #populate the values of the property form with current data
         prop.setPropertyForm(form,property_id)
    return render_template('administration/editProperty.html', form=form)


###############################
##########Content Pages#######
##############################
#These pages are for managing text and displays in the UI, also managing test sent in emails
@admin.route('/content', methods=['GET','POST'])
def content():
    content=Content()
    #load content template with emails content and UI content in tables

    return render_template('administration/config.html', email = content.getEmails(), content=content.getContent())


@admin.route('/editContent%<string:key>%<string:content_type>', methods=['GET','POST'])
def editContent(key,content_type):

    #edit the content by key that is passed through the URL
    form = ContentForm()
    content = Content()
    p= content.getContentById(key)

    if request.method=='POST':

        content.updateConfig(form)
        return redirect(url_for('admin.content'))
    #load the form with the current data of the content being edited.

    form.key.data = p[1]
    #the html is escaped in the DB so return to regular HTML
    form.subject.data = html.unescape(p[3])
    form.content.data = html.unescape(p[2])

    #load page with form and the content_type so that the subject field can be
    #disabled or enabled via javascript. UI content should not be able to add subject text
    return render_template('administration/editField.html', form=form, type=content_type)