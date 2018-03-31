import os
import unittest
import pymysql
import sys
from flask import session
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import app, DB, mail


class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        

        # Disable sending emails during unit testing
        mail.init_app(app)
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):

        pass
        
    def submitEvent(self,location,event_type,description):
        return self.app.post(
        '/event/event-request',
        data=dict(location=location,event_type=event_type,description=description),
        follow_redirects=True
    )
    def get_max_event_id(self):
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        con.execute("select max(EventId) from events")
        p = con.fetchone()
        return p[0]
    def add_event_data(self,event_id):
        return self.app.post(
            '/administration/event',
            data=dict( eventdate='9000-06-01', id=event_id, receipt=123456789049, invoice=9878987654566),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/auth/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
###############
#### tests ####
###############

    
     
    def test_event(self):
        response = self.app.get('/event/event-request', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome!', response.data)

#submit an event on the event request form.
    def test_event_form(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)

        response = self.submitEvent(1,2,'This is a test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Private event Request has been recieved', response.data)


#test adding a recipet number, schedule data, and invoice number from admin page
    def test_add_event_data_admin(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.add_event_data(self.get_max_event_id())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'9000-06-01', response.data)

if __name__ == "__main__":
    unittest.main()