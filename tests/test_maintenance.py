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
        
    def submitMaintenance(self,location,description):
        return self.app.post(
        '/maintenance/maintenance-request',
        data=dict(location=location,description=description),
        follow_redirects=True
    )
    def get_max_maintenance_id(self):
        conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3],autocommit=True)
        con = conn.cursor()
        #get all properties
        con.execute("select max(maitEventId) from maintenance_requests")

        p = con.fetchone()
        return p[0]

    def schedule_maintenance_request(self,maint_id):
        return self.app.post(
            '/administration/maintenance',
            data=dict( id=maint_id, dateofwork='9000-06-01'),
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

    
     
    def test_maintenance_page(self):
        
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/maintenance/maintenance-request', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    #test to see if a event request can be submitted by a user.
    def test_event_form(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.submitMaintenance(1,'This is a test main request')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Maintenance Request has been recieved', response.data)

    #maintenance requests are scheduled from the admin page. Get the last inserted id and 
    #pass it to the Schedule maintenace funtion. Pass a crazy number so it can be founr in page if 
    #it exists
    def test_schedule_maintenance_request(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        response = self.schedule_maintenance_request(self.get_max_maintenance_id())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'9000-06-01', response.data)

if __name__ == "__main__":
    unittest.main()