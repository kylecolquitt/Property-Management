import os
import unittest
import pymysql
import sys

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
    
    def register(self,first_name,last_name,organization,address,city, state, zipcode, email,phone, ext, password):
        return self.app.post(
        '/auth/register',
        data=dict(email=email, password=password,first_name=first_name,last_name=last_name,organization=organization,address=address,city=city, state=state, zip=zipcode,phone=phone, ext=ext),
        follow_redirects=True
    )
 
    def login(self, email, password):
        return self.app.post(
            '/auth/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
 
    def logout(self):
        return self.app.get(
            '/auth/logout',
            follow_redirects=True
        )

        

###############
#### tests ####
###############

    def test_db_connection(self):
        try:
            conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3])
            print('Database connected succesfully')
        except:
            print('Error connecting to db')

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

   #add a dupllicate email. Should not allow registration as email needs to be unique for login
    def test_invalid_user_registration(self):
        response = self.register('kyle','colq','PA', '111 Columbia','North Ogo', 'UT', 99939,'test@gmail.com',3553555555,444, 'testPassword')
        self.assertEqual(response.status_code, 200)
        response = self.register('kyle','colq','PA', '111 Columbia','North Ogo', 'UT', 99939,'test@gmail.com',3553555555,444, 'testPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Exists. Please login or click Forgot Password if you forgot your password', response.data)

    def test_user_login(self):
        response = self.login('admin@admin.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome!', response.data)

    #test several administrator pages to ensure that an unlogged in user can't access these pages.
    def test_access_page_restricted(self):
        response = self.app.get('/administration/event', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to access this page', response.data)
        response = self.app.get('/administration/maintenance', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to access this page', response.data)
        response = self.app.get('/administration/manageAdmin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to access this page', response.data)
        response = self.app.get('/administration/manageCustomers', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to access this page', response.data)
        response = self.app.get('/administration/properties', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not authorized to access this page', response.data)





    
if __name__ == "__main__":
    unittest.main()