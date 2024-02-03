'''Presets for creating databases'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from flask_httpauth  import HTTPTokenAuth, HTTPBasicAuth

import secrets
ma = Marshmallow()
db = SQLAlchemy()


class Permission: #Permission Constants - BITWISE
    '''Varying permission levels to be assigned individually or to Roles'''
    PUBLIC = 1    # 0b00001
    STUDENT = 2   # 0b00010
    CLASS = 4     # 0b00100
    GRADE = 8     # 0b01000
    SCHOOL = 16   # 0b10000
    DISTRICT = 32 # 0b100000
    YOY = 64      # 0b1000000


class Role(db.Model):
    '''Associate permissions with roles, add and remove permissions from roles'''
    __tablename__ ='roles'
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, default ='User')
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.permissions

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.PUBLIC],
            'Teacher':[Permission.STUDENT, Permission.CLASS],
            'Principal':[Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.YOY],
            'Admin': [Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.DISTRICT, Permission.YOY]
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()


class Staff(db.Model):
    '''Checks Staff table for new user pre-assigned role, also can update and remove roles '''
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user_id = db.relationship('User', backref='staff', uselist=False)

    

    def __init__(self, staff_id, email, role_id):
        self.staff_id = staff_id
        self.email = email
        self.role_id = role_id

    

class User(db.Model):
    '''Creates user accounts and stores user info'''
    __tablename__ ='users'
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(150), nullable = False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, password='', first_name = '', last_name = '', email = '', role= 1, token='', g_auth_verify=False):
        self.user_id = self.set_id()
        self.username = self.create_username()
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify   

    #CREATE USER NAME, PASSWORD     
    def create_username(first_name, last_name):
        base_username = (first_name[0] + last_name).lower()
        username = base_username
        suffix = 1
        while User.query.filter_by(username=username).first() is not None:
            username = f"{base_username}{suffix}"
            suffix += 1
        return username
    pass

    def __repr__(self):
        return '<User %r>' % self.username

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    @staticmethod
    def set_password(password):
        return generate_password_hash(password)
    
    def check_password(self, plain_text_password):
        return check_password_hash(self.password, plain_text_password)
    
    def __repr__(self):
        return f'User {self.username} has been added to the database'
    
    #USER ROLES
    def get_roles(self):
        role = db.session.execute(db.select(Role.name).where(User.role_id == Role.id))
        return role

    def edit_user_role(self, role_id):
        if not self.has_role(role_id):
            self.role_id = role_id
            return self.role_id
    
    def has_role(self, role_id):
        if self.role_id:
            return self.role_id == role_id
        else:
            return None 

    #PERMISSIONS 
    def has_permission(self, perm):
        role = Role.query.get(self.role_id)
        if role is not None:
            return role.permissions & perm == perm
        else:
            return None
        
    def assigned_classrooms(self):
        if self.has_permission(Permission.CLASS):
            teacher_assignments = ClassroomSchoolYear.query.filter_by(teacher_id=self.staff_id).all()
            for assignment in teacher_assignments:
                self.follow_classrooms(assignment.id) #add view?

    def assigned_schools(self):
        if self.has_permission(Permission.SCHOOL):
            principal_assignments = SchoolYear.query.filter_by(principal_id=self.staff_id).all()
            for assignment in principal_assignments:
                self.follow_school(assignment.school_id)

    def follow_classrooms(self, classroom_schoolyear_id):
        if not self.is_following(classroom_schoolyear_id):
            f=UserClassroom(user_id= self,classroom_schoolyear_id = ClassroomSchoolYear.id)
            db.sessions.add(f)

    def follow_school(self, school_id):
        recent_school_year = SchoolYear.query.filter_by(school_id=school_id).order_by(SchoolYear.year_id.desc()).first()
        if recent_school_year and recent_school_year.principal_id == self.user_id:
            return True
        else:
            return False

    def unfollow_classroom(self,classroom_view):
        f = self.classroom_views.filter_by(classroom_view = classroom_view.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, classroom_view):
        if classroom_view.id is None:
            return False
        return self.classroom_views.filter_by(classroom_view = classroom_view.id).first() is not None




class School(db.Model):
     '''Unique ids for each school in the WCSU'''
     __tablename__ = 'schools'
     id = db.Column(db.String(10), primary_key=True)
     name = db.Column(db.String(100), unique=True, nullable=False)
     short_name = db.Column(db.String(50), unique=True, nullable=False)

     def __init__(self, id, name, short_name):
         self.id = id
         self.school_name = name
         self.short_name = short_name

class Year(db.Model):
    '''Year table to separate instances of classes and students over years'''
    __tablename__='years'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    schools = db.relationship('School',
                              secondary = 'school_years',
                              backref=db.backref('years', lazy='dynamic'),
                              lazy='dynamic') #open relationship between year and school

    def __init__(self, id, start_date, end_date):
        self.year_id = id
        self.start_date = start_date
        self.end_date = end_date


class GradeLevel (db.Model):
    '''School grade levels -1 (PK) to 12'''
    __tablename__= 'grade_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)    

    def __init__(self, id, name):
        self.id = id
        self.name = name



class Period (db.Model): 
    __tablename__='periods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)

class SchoolYear(db.Model):
    '''Associate school years with schools, prinicpals and superintendents'''
    __tablename__='schoolyears'
    id = db.Column(db.String(100), primary_key = True)
    school_id = db.Column(db.String(10), db.ForeignKey('schools.id'))
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'))
    principal_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    super_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

class Classroom(db.Model):
    '''Creates a table for each classroom in a school '''
    __tablename__ = 'classrooms'
    id = db.Column(db.String(50), primary_key = True)
    subject = db.Column(db.String(150), nullable = True)
    school_id = db.Column(db.String(50), db.ForeignKey('schools.id'))
    grade_level_id = db.Column(db.Integer, db.ForeignKey('grade_levels.id'))
    years = db.relationship('Year',
                              secondary = 'classroom_schoolyears',
                              backref=db.backref('years', lazy='dynamic'),
                              lazy='dynamic') 

    def __init__(self, id, subject):
        self.id = id
        self.subject = subject

class ClassroomSchoolYear(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    __tablename__ = 'classroom_schoolyears'
    id = db.Column(db.String(150), primary_key=True)
    classroom_id = db.Column(db.String(50), db.ForeignKey('classrooms.id'))
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

    def __init__(self, classroom_id, year_id):
        self.classroom_id = classroom_id
        self.year_id = year_id

    #def add_year.. >append
# classroom_periods = db.Table('classroom_periods',
#                        db.Column('classroom_schoolyear_id', db.String(10), db.ForeignKey('classroom_schoolyears.id')),
#                        db.Column('period', db.Integer, db.ForeignKey('period.id'))
#                        )

class UserClassroom(db.Model):
    '''Users are associated with classroom schoolyear'''
    __tablename__ = 'user_classrooms'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    classroom_id = db.Column(db.String(50), db.ForeignKey('classrooms.id'))
    classroom_schoolyear_id = db.Column(db.String(150), db.ForeignKey('classroom_schoolyears.id'))

    # Relationships
    classroom = db.relationship('Classroom', backref='user_classrooms')
    classroom_school_year = db.relationship('ClassroomSchoolYear', backref='user_classrooms')

    def __init__(self, user_id, classroom_id, classroom_schoolyear_id=None):
        self.user_id = user_id
        self.classroom_id = classroom_id
        self.classroom_school_year_id = classroom_schoolyear_id

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key = True)
    student_first = db.Column(db.String(100))
    student_last = db.Column(db.String(100))

class Assessment(db.Model):
    '''general information about each assessment'''
    __tablename__='assessments'
    id = db.Column(db.String(25),primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)	
    short_name = db.Column(db.String(10), unique = True, nullable = False)	
    family = db.Column(db.String(100))
    type = db.Column(db.String(100))	
    subject = db.Column(db.String(100))	
    content_standard = db.Column(db.String(100))

    def init(self, id, name, short_name, family, type, subject, content_standard):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.family = family
        self.type = type
        self.subject = subject
        self.content_standard = content_standard

class AssessmentStandard(db.Model):
    '''Benchmark scores for tier 1, 2, 3'''
    __tablename__='assessment_standards'
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    rank_score = db.Column(db.Float(5,2))	
    assessment_id = db.Column(db.String(25), db.ForeignKey('assessments.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))	
    grade_level_id = db.Column(db.Integer, db.ForeignKey('grade_levels.id'))

    def __init__(self, id, rank, rank_score, assessment_id, period_id, grade_level_id):
        self.id = id
        self.rank = rank
        self.rank_score = rank_score
        self.assessment_id = assessment_id
        self.period_id = period_id
        self.grade_level_id = grade_level_id

class AssessmentScores(db.Model):
    '''Student assessment scores'''
    __tablename__ = 'assessment_scores'
    id = db.Column(db.String, primary_key=True)
    score = db.Column(db.Float(5,2))
    classroom_schoolyear_id = db.Column(db.String)
    assessment_id = db.Column(db.String(25), db.ForeignKey('assessments.id') )
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

