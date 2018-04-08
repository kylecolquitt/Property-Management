from app import app,DB
import pymysql
from flask import session,redirect,url_for
from app.google.views import create

#this class handles the administration and submitting of a private event request
class Event:

    #get all current private event requests from the data base.
    def getRequest(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #get all events from event view that are not scheduled or the event date has not passed. these will be displayed in the
        #current events table in the template.
        con.execute("select * from event_management where DateOfEvent >= CURDATE() - interval 1 day or DateOfEvent = '0000-00-00'")
        event = con.fetchall()
        requests = []
        #create a list of dictionaries so event information can be used in system
        for row in event:
            req = {'FirstName' : row[1], 'LastName': row[2], 'Email': row[3], 'Phone': row[4], 'Property':row[5], 'Type':row[7], 'date':row[8], 'Reciept':row[10], 'Invoice':row[9],'Description':row[11], 'ID': row[0]}
            requests.append(req)
        con.close()
        return requests

    #get all events that have passed. This is based on the current date.
    def getPastEvents(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #get all events from event view that are not passed and make sure they are not unscheduled events.
        con.execute("select * from event_management where DateOfEvent < CURDATE() - Interval 1 day and DateOfEvent != '0000-00-00'")
        event = con.fetchall()
        requests = []
        #create a list of dictionaries so event information can be used in system
        for row in event:
            req = {'FirstName' : row[1], 'LastName': row[2], 'Email': row[3], 'Phone': row[4], 'Property':row[5], 'Type':row[7], 'date':row[8], 'Reciept':row[10], 'Invoice':row[9],'Description':row[11], 'ID': row[0]}
            requests.append(req)
        con.close()
        return requests
    
    #add a new request to the events table in the database
    def addRequest(self,form):
        #add new event request to database
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("INSERT INTO events (PropId, CustomerId, DateOfEvent, description, EventType) VALUES (%s,%s,%s,%s,%s)" , (form.location.data, session['person_id'], '10/10/2010', form.description.data, form.event_type.data))
            con.close()
        except:
            print('Failure when creating event request')
        return form

    #function to add event data from admin page. This adds the receipt, invoice and dateofwork to the existing row
    def addInvRec(self,form):
        event = None
        try:
            #try to insert new form data entered on manage event request page
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("select * from event_management WHERE EventID = %s", (form.id.data))
            event = con.fetchone()
            con.execute("UPDATE events SET InvoiceNumber=%s, ReceiptNumber=%s, DateOfEvent=%s WHERE EventID = %s", (form.invoice.data if form.invoice.data != '' else event[9], form.receipt.data if form.receipt.data != '' else event[10],form.eventdate.data if form.eventdate.data is not None else event[8], form.id.data))

            con.close()

        except:
            print('Failed to add invoice and receipt information.')

        if form.eventdate.data != None:
            event_id = 'bradsha' + str(event[0])
            calendar_event = {
                'summary': event[5],
                'id': event_id,
                'location': event[5],
                'description': 'Requester: ' + event[1] + ' ' + event[2] +'<br>'+ event[3] +'<br>' + event[4] + '<br>Event Type:' + event[7] + '<br><br>Comments:<br>' + event[11] ,
                'start': {
                    'date': str(form.eventdate.data if form.eventdate.data != '' else event[8]),
                },
                'end': {
                    'date': str(form.eventdate.data if form.eventdate.data != '' else event[8]),
                },

                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }
        else:
            calendar_event =None

        return calendar_event


#get all properties for use in the form dropdowns.
def getProperties():
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #get all properties
        con.execute("SELECT * FROM property")
        p = con.fetchall()
        property_list=[]
        
        #add a default so first value in database is not default
        prop ={'ID':0, 'Address':'-'}
        property_list.append(prop)

        #create a list of dictionaries so property information can be used in system
        for row in p:
            address= row[2] +' ' + row[3]  + ', ' + row[4] + ' ' + row[5]
            prop = {'ID' : row[0],'Address': address}
            property_list.append(prop)
        con.close()
        return property_list

#get event types for use in the event form dropdown
def getEventType():
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #get all event types
        con.execute("SELECT * FROM event_type ")
        event_list=[]
        c = con.fetchall()

        #add a default so first value in database is not default
        default ={'ID':0, 'Type':'-'}
        event_list.append(default)

        #create a list of dictionaries so event_type information can be used in system
        for row in c:
            event = {'ID' : row[0],'Type': row[1] }
            event_list.append(event)
        con.close()
        return event_list