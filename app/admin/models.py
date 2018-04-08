from app import app,DB, MAIL_USERNAME,mail
import pymysql
import html
from flask_mail import Message
from flask import render_template,session


class Admin:

    #function to load all administrators and corresponding data associated with them
    def getAdmins(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all admins
        con.execute("SELECT * FROM customer join Customer_Type on Customer.CustType=Customer_Type.CustType WHERE customer.CUSTTYPE=3")
        user = con.fetchall()
        admins=[]
        #create a list of dictionaries so admin information can be used in system
        for row in user:
            adm = {'FirstName' : row[1], 'LastName': row[2], 'Organization': row[3], 'Address' : row[4], 'City': row[5], 'State': row[6], 'Zip Code': row[7],'Email' : row[8], 'Phone': row[9], 'Extension': row[10], 'User_Type': row[14],'ID': row[0]}
            admins.append(adm)
        con.close()
        return admins

    #function to load all customers and corresponding data associated with them. Table joined to get there role names
    def getCustomers(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all admins
        con.execute("SELECT * FROM customer join Customer_Type on Customer.CustType=Customer_Type.CustType WHERE customer.CUSTTYPE!=3")
        user = con.fetchall()
        admins=[]
        #create a list of dictionaries so admin information can be used in system
        for row in user:
            adm = {'FirstName' : row[1], 'LastName': row[2], 'Organization': row[3], 'Address' : row[4], 'City': row[5], 'State': row[6], 'Zip_Code': row[7],'Email' : row[8], 'Phone': row[9], 'Extension': row[10], 'User_Type': row[14],'ID': row[0]}
            admins.append(adm)
        con.close()
        return admins

    #loads the emails for all administrators in the system    
    def getEmail(self):
        #get admins from DB
        admins = self.getAdmins()

        emails=[]
        x=0
        for row in admins:
            #get each admin out of list
            ad = admins[x]
            x = x+1
            #add email of admin to emails list
            emails.append(ad['Email'])
        return emails

    #get the default email recipient emails. These are the emails that will recieve emails for new requests.
    def getDefaultEmails(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all emails
        con.execute("SELECT * FROM default_recipient")
        email = con.fetchall()
       
       #returns the email and their ids
        return email

    #get the email address list from db. Default email recipients
    def getEmailList(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all admins
        con.execute("SELECT * FROM default_recipient")
        email = con.fetchall()
        emails=[]
        for row in email:        
            emails.append(row[1])

        #only returns the addres, not the emails id in the database
        return emails

    #add new email as a default recipient for system emails
    def addEmail(self,form):
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("INSERT INTO default_recipient (Email) VALUES (%s)" , (form.email.data))
            con.close()

        except:
            print('failure when adding email to default_recipients')
        return None

    #update the customer in the system
    def updatePerson(self,form, person_id):
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            if form.custtype.data == 0:
                con.execute("UPDATE customer SET FirstName=%s, LastName=%s, Organization=%s,Address=%s,City=%s, State=%s, Zip=%s, Email=%s, Phone=%s, Extension=%s WHERE CustomerId = %s", (form.first_name.data,form.last_name.data, form.organization.data,form.address.data,form.city.data, form.state.data,form.zip.data,form.email.data, form.phone.data,form.ext.data, person_id))
            else:
                con.execute("UPDATE Customer SET FirstName=%s, LastName=%s, Organization=%s,Address=%s,City=%s, State=%s, Zip=%s, Email=%s, Phone=%s, Extension=%s, CustType=%s WHERE CustomerId = %s", (form.first_name.data,form.last_name.data, form.organization.data,form.address.data,form.city.data, form.state.data,form.zip.data,form.email.data, form.phone.data,form.ext.data, form.custtype.data, person_id))
            con.close()

        except:
            print('Tried to add the same email address.')
        return None

    
    #delete an email from the list of default recipients
    def deleteEmail(self,id):
        try:
            #try to delete admin
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            sql = "DELETE FROM default_recipient WHERE ID = %s" 

            con.execute(sql, id)
            con.close()

        except:
            print('Delete Failed')
        return None


    #get a person from the db and their information by ther person Id
    def getPersonById(self,person_id):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get user
        con.execute("SELECT * FROM Customer WHERE CustomerId = %s", person_id )
        user = con.fetchone()
        con.close()

        return user

    #set the edit person form with a user's information in the Database
    def setPersonForm(self,form,person_id):
        admin = self.getPersonById(person_id)

        form.first_name.data = admin[1]
        form.last_name.data = admin[2]
        form.organization.data = admin[4]
        form.address.data = admin[4]
        form.city.data = admin[5]
        form.state.data = admin[6]
        form.zip.data = admin[7]
        form.email.data = admin[8]
        form.phone.data = admin[9]
        form.ext.data = admin[10]
        form.custtype.data = admin[11]
      
        return None
        
class Property:

    #loads all properties from the database
    def getProperties(self, archived_status):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all properties
        con.execute("SELECT * FROM property")

        p = con.fetchall()
        property_list=[]
        #create a list of dictionaries so admin information can be used in system
        for row in p:
            prop = {'ID' : row[0], 'Description' : row[1], 'Address': row[2], 'City': row[3], 'State': row[4], 'Zip' : row[5], 'Type' : row[6]}
            property_list.append(prop)
        con.close()
        return property_list
    
    #add a new property to the table. 
    def addProperty(self,form):
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("INSERT INTO property (Description, Address, City, State, Zip, Type) VALUES (%s, %s,%s,%s, %s,%s)" , (form.description.data, form.address.data, form.city.data, form.state.data, form.zip.data, form.p_type.data))
            con.close()

        except:
            print('failure when creating property')
        return None

    #edit current property information
    def updateProperty(self,form, property_id):
        try:
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("UPDATE property SET Description=%s, Address=%s, City=%s, State=%s, Zip=%s, Type=%s WHERE PropertyID = %s", (form.description.data, form.address.data, form.city.data, form.state.data, form.zip.data, form.p_type.data, property_id))
            con.close()

        except:
            print('Failed to add property')
        return None
    

    #load a property by its database id
    def getPropertyById(self,property_id):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get user
        con.execute("SELECT * FROM property WHERE PropertyId = %s", property_id )
        user = con.fetchone()
        con.close()

        return user

    #set the values on the edit property form with that properties current data.
    def setPropertyForm(self,form,property_id):
        #get the property by its id
        admin = self.getPropertyById(property_id)
        form.description.data = admin[1]
        form.address.data = admin[2]
        form.city.data = admin[3]
        form.state.data = admin[4]
        form.zip.data = admin[5]
        form.p_type.data = admin[6]
        return None

class Content():

    # get the system emails to be modified by admin
    def getEmails(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all emails
        #emails have subject text in the database so they are queried for having subject data
        con.execute("SELECT * FROM config where subject !=''")

        p = con.fetchall()
        email_list=[]
        #create a list of dictionaries so emails information can be used in system
        for row in p:
            email = {'ID' : row[0], 'key' : row[1], 'content': html.unescape(row[2]), 'subject': html.unescape(row[3]), 'description': html.unescape(row[4])}
            email_list.append(email)
        con.close()
        return email_list
    
        #load UI content from the database to be edited by admin
    def getContent(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all content
        #UI content does not have subject data. It is blank. This is how they are distinguished from the
        #emails in this table
        con.execute("SELECT * FROM config where subject=''")

        p = con.fetchall()
        content_list=[]
        #create a list of dictionaries so content information can be used in system
        for row in p:
            content = {'ID' : row[0], 'key' : row[1], 'content': html.unescape(row[2]), 'subject': html.unescape(row[3]), 'description': html.unescape(row[4])}
            content_list.append(content)
        con.close()
        return content_list

    #update the content edited through the UI
    def updateConfig(self,form):
        try:
            import html
            #try to insert new form data
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("UPDATE config SET `text`=%s, `subject`=%s WHERE `key` = %s", (html.escape(form.content.data), html.escape(form.subject.data), form.key.data))
            con.close()
        except:
            print('Failed to update config')
        return None

    #get content by its key
    def getContentById(self, key):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all emails
        con.execute("SELECT * FROM config where `key` =%s",(key))

        p = con.fetchone()
        
        return p

#get all customer type/roles from the database to be used in the edit person form
def getCustomerType():
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        con.execute("SELECT * FROM customer_type")

        c = con.fetchall()
        customer_type_list=[]
        customer ={'ID':0, 'Type':'-'}
        customer_type_list.append(customer)
        for row in c:
            customer_type = {'ID' : row[0],'Type': row[1]}
            customer_type_list.append(customer_type)
        con.close()
        return customer_type_list

#load customer type by its id
def getCustomerTypeBId(person_id):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all admins
        con.execute("SELECT Type FROM customer_type  WHERE CustType in (SELECT CustType from customer WHERE CustomerID = %s)",(person_id))

        c = con.fetchone()

        #create a list of dictionaries so admin information can be used in system
        return c[0]


#email sent to the admin when a new maintenance or event request is submitted by a user
def sendAdminEmail(key,form):
    email = Content()
    admin=Admin()
    prop = Property()

    #get email by the content key passed to function
    x=email.getContentById(key)

    #get all the default admin emails who will recieve new email
    emails = admin.getEmailList()

    #msg include the email subject, and load the template that displays the custom email content and the event details. This part
    #of email cant be edited.
    msg = Message(x[3],
        sender=MAIL_USERNAME,
        recipients=emails)
    msg.body=render_template('email/basicEmail.html',form=form, requester=session['name'], add=session['email'],location=prop.getPropertyById(form.location.data), email=html.unescape(x[2]))
    msg.html=render_template('email/basicEmail.html',form=form,requester=session['name'], add=session['email'], location=prop.getPropertyById(form.location.data), email=html.unescape(x[2]))
    mail.send(msg)
    return None


#send email to users when a new request is submitted. 
def sendUserEmail(key,form):
    email = Content()
    prop = Property()

    #load email content by the key passed into the form
    x=email.getContentById(key)
    
    msg = Message(x[3],
        sender=MAIL_USERNAME,
        #use the users session email as the recipient
        recipients=[session['email']])
    #msg include the email subject, and load the template that displays the custom email content and the event details. This part
    #of email cant be edited.
    msg.body=render_template('email/basicEmail.html',form=form, requester=session['name'], add=session['email'],location=prop.getPropertyById(form.location.data), email=html.unescape(x[2]))
    msg.html=render_template('email/basicEmail.html',form=form,requester=session['name'], add=session['email'], location=prop.getPropertyById(form.location.data), email=html.unescape(x[2]))
    mail.send(msg)
    return None