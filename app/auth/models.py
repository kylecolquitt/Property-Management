from app import app,ADMINS,DB,bcrypt
import pymysql
from flask import session, g
import json
import datetime

class User:


    #get administrators in the system for managing on manage admins page.
    def getAdmins(self):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #select all users with a user type of Administrator
        con.execute("SELECT * FROM customer WHERE CUSTYPE=3")
        user = con.fetchall()

        #create a list
        admins=[]
        for row in user:

            #add each user to a dict and append to list
            adm = {'FirstName' : row[1], 'LastName': row[2], 'Email': row[3]}
            admins.append(adm)
        con.close()
        return admins
    

    def checkLogin(self,form):
        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        
        #get user credentials where email = submitted email
        con.execute("SELECT * FROM customer where Email = %s", (form.email.data))
        user = con.fetchone()
        #if the hashed password matches the submitted password
        if bcrypt.check_password_hash(user[12], form.password.data):

            #set the user type so user sees appropriate tabs
            session['role'] = user[11]

            #return user data
            return user
        else:

            #the users information was incorret
            return None

    #function to check if email already exists in the system. Called by the register function
    #to ensure that all emails in the system are unique
    def checkEmail(self,email):

        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #check to see if email exists in the system
        con.execute("SELECT * FROM customer where Email = %s", (email))
        user = con.fetchall()

        # if email exists
        if user != None:
            return True
        else:

            #email does not exist
            return False
        con.close()

    #get user by their email
    def getUser(self,form):

        #connect
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()

        #get user by email
        con.execute("SELECT * FROM customer where Email = %s", (form.email.data))
        user = con.fetchone()
        return user

    #register new user
    def addUser(self,form):
        try:
            #try to add user data

            #connect
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            #insert form values
            con.execute("INSERT INTO customer (FirstName, LastName, Organization, Address, City, State,Zip,Email,Phone,Extension,Password) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s)" , (form.first_name.data, form.last_name.data,form.organization.data,form.address.data,form.city.data,form.state.data,form.zip.data,form.email.data,form.phone.data,form.ext.data, bcrypt.generate_password_hash(form.password.data)))
            con.close()
        except:
            print('failure when adding new user')
        return None
    

    #function to add generated token from the forgot password page. Add this token to the database,
    #so it can be checked when user accesses the emailed link
    def addToken(self,person_id, token):

        #add token to database when user has forgotten password
        try:

            #try to add token and person id
            #connect
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()
            con.execute("INSERT INTO forgot_password (PersonId, CreateDate, Token) VALUES (%s, %s,%s)" , (person_id, datetime.datetime.now(), bcrypt.generate_password_hash(token)))
            con.close()

        except:
            print('failure when adding token')
        return None


    #check the token from the reset password link to make sure it is not expired,
    #or non-existent
    def checkToken(self,person_id,token):

        #validate token in url and DB
        try:

            #get the token stored in the database by the user for checking
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()

            con.execute("SELECT * FROM forgot_password WHERE PersonId = %s" , (person_id))
            hashed_token = con.fetchone()

            #token expires in 3 hours. get current time minus 3 hours and compare
            from datetime import datetime, timedelta
            last_hour_date_time = datetime.now() - timedelta(hours = 3)

            #if the token is not expired, check the token against the usrl
            if hashed_token[3] > last_hour_date_time:            

            #check token from url and hashed token from db
                if bcrypt.check_password_hash(hashed_token[2], token):
                    
                    #if they match return true to load password page
                    return True
                else:

                    #else no
                    return False
            else:
                #the token is non-existent or expired row from database
                self.deleteToken(person_id)
            con.close()

        except:
            print('failure when getting token')
        return None
    
    #delete entry associated with a user from the forgot_password table
    #a user can't have more than one row associated with a person id
    def deleteToken(self,person_id):
        try:
            #remove token once user has accessed the page
            #connect
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()

            #delete token asociated with person id
            con.execute("DELETE FROM forgot_password WHERE PersonId = %s" , (person_id))
            con.close()

        except:
            print('failure when deleteing token')
        return None
    
    #if the token and url are correct. The change password form is loaded. If passwords match
    #this function updates the password in the customer table associated with user id from url
    def updatePassword(self,person_id,password):
        try:
            #update password changed on password reset page

            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
            con = conn.cursor()

            #update user in database with new hashed password
            con.execute("UPDATE customer SET PASSWORD=%s WHERE CUSTOMERID = %s" , (bcrypt.generate_password_hash(password), person_id ))
            con.close()

            #delete token from database
            self.deleteToken(person_id)

        except:
            print('failure when adding password')
        return None
