import unittest
from app import create_app, db
from models import User, Staff, Student, AssessmentScore, AssessmentStandard, StudentClassroomAssociation, Classroom, AssessmentStandard, AssessmentScore

import unittest
from app import db, current_user, Staff, Classroom, ClassStudent, StudentScoreForm, component_dict, new_assessment_grades

class TestEnterStudentGrades(unittest.TestCase):

    def setUp(self):
        # Initialize the database and create test data
        self.app = create_app()
        self.client = self.app.test_client
        self.app.app_context().push()
        db.create_all()

        # Create test data
        staff = Staff(id=1, username='test_user', password='test_password')
        db.session.add(staff)
        db.session.commit()

        classroom = Classroom(id=1, staff_id=1, name='Test Classroom')
        db.session.add(classroom)
        db.session.commit()

        student1 = ClassStudent(id=1, full_name='Student 1', class_id=1)
        student2 = ClassStudent(id=2, full_name='Student 2', class_id=1)
        db.session.add_all([student1, student2])
        db.session.commit()

        comp_dict = component_dict('Predictive Assessment of Reading', 1)

    def test_enter_student_grades_with_existing_scores(self):
        # Create test data
        current_score1 = AssessmentScore(id=1, student_id=1, classroom_id=1, period=1, assessment_id=1, student_score=10)
        current_score2 = AssessmentScore(id=2, student_id=2, classroom_id=1, period=1, assessment_id=1, student_score=20)
        db.session.add_all([current_score1, current_score2])
        db.session.commit()

        # Call the function
        result = enter_student_grades(request)

        # Assert that the function returns a redirect to the data entry page
        self.assertEqual(result, redirect(url_for('data.data_entry', username='test_user')))

    def test_enter_student_grades_without_existing_scores(self):
        # Call the function
        result = enter_student_grades(request)

        # Assert that the function creates and commits new AssessmentScore objects
        self.assertEqual(len(db.session.new_state), 2)

    def tearDown(self):
        # Clean up the test data
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()