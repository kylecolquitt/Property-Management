from app import app,DB
from flask import session
import pymysql

#This class handles everything related to the administration and submitting of a maintenance request.
class Maintenance:

    #Get maintenance requests from database by completion type. Store each request in a list of dictionaries
    def getRequest(self, complete):

        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        
        #get maintenance requests by completeion. if completeion = 1, query database for completion columns = 'yes'
        if complete==1:
            complete = 'Yes'
        else:
            complete='No'
    
        con.execute("select * from manage_maintenance where complete =%s", complete)

        #get all the data
        main = con.fetchall()
        requests = []
        #create a list of dictionaries of maintenance request and columns
        for row in main:
            req = {'FirstName' : row[1], 'LastName': row[2], 'Email': row[3], 'Phone': row[4], 'Property':row[5], 'Description':row[6], 'ID': row[0], 'DateofWork': row[7]}
            requests.append(req)
        con.close()
        return requests
    
    #add a new maintenance request to the database
    def addRequest(self,form):
        #add a request
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("INSERT INTO MAINTENANCE_REQUESTS (PropertyId, CustomerId, WorkDescription) VALUES (%s, %s,%s)" , (form.location.data, session['person_id'], form.description.data))
            con.close()

        except:
            print('Failure when trying to add maintenance request.')
        return None

    #once an admin has completed a maintenance request, mark the request completed. This function also handled
    #undoing mark complete do the request shows as in progress.
    def markComplete(self, maintenance_id, complete):
        #connect

        #once a maintenance request has been completed. Update the complete column to 'yes'

        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        if complete == 1:
            complete = 'Yes'
        else:
            complete = 'No'
        try:
            #try to update complete column

            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            sql = "UPDATE MAINTENANCE_REQUESTS SET COMPLETE = %s WHERE MaitEventId = %s" 
            con.execute(sql, (complete,maintenance_id))
            con.close()

        except:
            print('Failed to update completion of a maintenance request')
        return None

    #Admin schedules a date for a request. 
    def scheduleRequest(self,form):
        #Schedule a request to be emailed and added to calendar
        try:
            #try to insert update date of work
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("UPDATE MAINTENANCE_REQUESTS SET DateOfWork=%s WHERE MaitEventId = %s", (form.dateofwork.data, form.id.data))
            con.close()

        except:
            print('Failed to Schedule Maintenance')
        return None

#Used for forms
#load all properties from database for use in dropdowns.
def getProperties():
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all properties
        con.execute("SELECT * FROM PROPERTY")

        p = con.fetchall()
        property_list=[]
        #add a default that is not selectable so the first property in the table is not default. 
        #Give an ID of 0 because ids in the database start at 1
        prop ={'ID':0, 'Address':'-'}
        property_list.append(prop)
        #create a list of dictionaries so property information can be used in system
        for row in p:
            address= row[2] +' ' + row[3]  + ', ' + row[4] + ' ' + row[5]
            prop = {'ID' : row[0],'Address': row[1] + ' - ' + address }
            property_list.append(prop)
        con.close()
        
        return property_list