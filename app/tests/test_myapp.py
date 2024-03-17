from flask_testing import TestCase
from flask import Flask
from app import init_app
from config import TestingConfig
from models import *
from flask_login import current_user

class MyTest(TestCase):

    def create_app(self):
        """
        Create the Flask app for testing
        """
        app = Flask(__name__)
        app.config.from_object(TestingConfig)  
        db.init_app(app)
        return app
    
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        super().setUp()
        self.app = self.create_app()
        with self.app.app_context():
            db.create_all()
            self.populate_db()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        with self.app.app_context():
            db.session.rollback() 
            db.drop_all()
        super().tearDown()
    
    def populate_db(self):
        """
        Populate the database with test data
        """
        # Insert test data as necessary
        pass

    def test_generate_profile_data(self):
        with self.client:
            # Log in as the test user (assuming you have a test user)
            response = self.client.post('/login', data=dict(
                username='rkelly@windhamcentral.org',
                password='rkelly123'
            ), follow_redirects=True)

            # Make sure the login was successful (assert response status code)
            self.assertEqual(response.status_code, 200)

            # Call the function to generate profile data
            profile_data = generate_profile_data()

            # Assert that the generated profile data is as expected
            expected_profile_data = {
                'rkelly': {
                    'name': ['Richard Kelly'],  # Replace with expected name
                    'school': ['PS177']  # Replace with expected school ID
                }
            }
            self.assertEqual(profile_data, expected_profile_data)



def generate_profile_data(self):
    '''Get user role and school association, associated classrooms, and class rosters(names of students in each class)'''
    #dict to store user info, role & school
    profile_data = {}
    classrooms = {}
    if current_user.is_staff_member & current_user.role_id == 2:
        user_classrooms = db.session.query(
            ClassroomSchoolYear).filter(
                ClassroomSchoolYear.teacher_id == self.staff_id)
        current_classroom = pd.DataFrame([uc for uc in user_classrooms]).sort_values('year_id', ascending=False)
        classrooms.update(c for c in current_classroom)
        cc = current_classroom[0]
        id = current_user.username
        profile_data[id] = {
            'name': [f'{current_user.first_name} {current_user.last_name}'],
            'school' : [cc.school_id]
        }