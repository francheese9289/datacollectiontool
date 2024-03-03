from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import uuid 
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()


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
    role_name = db.Column(db.String(150), nullable=False, default ='User')
    permissions = db.Column(db.Integer)

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
            role = Role.query.get(r)
            if role is None:
                role = Role(role_name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()



class Staff(db.Model):
    '''Checks Staff table for new user pre-assigned role, also can update and remove roles '''
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True, default='')
    last_name = db.Column(db.String(50), nullable=True, default='')
    staff_full_name = db.Column(db.String(150))
    email = db.Column(db.String(319), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, staff_id, first_name, last_name, staff_full_name, email, role_id):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name
        self.staff_full_name = staff_full_name
        self.email = email
        self.role_id = role_id


class User(db.Model, UserMixin):
    '''Creates user accounts and stores user info'''

    __tablename__ ='users'

    user_id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(319), nullable = False)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    staff_member = db.Column(db.Boolean, default = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))


    def __init__(self, email, first_name, last_name, password, role_id=1, staff_id=0):
        print(f'Init called with email: {email}, first_name: {first_name}, last_name: {last_name}') 
        
        self.user_id = self.set_id()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        print(f'Before create_username: {self.first_name}, {self.last_name}') 
        self.password = self.set_password(password) if password else ''
        self.username = self.create_username()
        print(f'After create_username: {self.username}')
        user_staff_info = self.is_staff_member(email)
        self.staff_id = user_staff_info['staff_id']
        self.role_id = user_staff_info['role_id']
        self.staff_member = user_staff_info['staff_member']

    def create_username(self):
        print(f'create_username called with first_name: {self.first_name}, last_name: {self.last_name}') 
        base_username = (self.first_name[0] + self.last_name).lower()
        username = base_username
        suffix = 1
        while User.query.filter_by(username=username).first() is not None:
            username = f"{base_username}{suffix}"
            suffix += 1
        self.username = username
        return username


    def __repr__(self):
        return '<User %r>' % self.username

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')


    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    #checks to see if user is staff member when creating an account
    def is_staff_member(self,email):
        staff_member = Staff.query.filter_by(email=email).with_entities(Staff.role_id, Staff.staff_id).first()
        if staff_member:
            staff_id = staff_member.staff_id
            role_id = staff_member.role_id
            user_staff= {'staff_id':staff_id,
                         'role_id': role_id,
                         'staff_member': True}
        else:
            user_staff={'staff_id':0,
                        'role_id':1,
                        'staff_member': False}

        return user_staff
            
class School(db.Model):
     '''Unique ids for each school in the WCSU'''
     __tablename__ = 'schools'
     id = db.Column(db.String(10), primary_key=True)
     name = db.Column(db.String(30), unique=True, nullable=False)
     short_name = db.Column(db.String(), unique=True, nullable=False)
    
     def __init__(self, id, name, short_name):
         self.id = id
         self.name = name
         self.short_name = short_name

     def __repr__(self):
        return '<School %r>' % self.name

class Year(db.Model):
    '''Year table to separate instances of classes and students over years'''
    __tablename__='years'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)


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
    __tablename__='school_years'
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
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
  
    def __init__(self, classroom_id, year_id):
        self.classroom_id = classroom_id
        self.year_id = year_id


class ClassroomSchoolYearPeriod(db.Model):
    __tablename__='classroom_schoolyear_periods'
    id = db.Column(db.String(100), primary_key=True)
    period = db.Column(db.Integer, db.ForeignKey('periods.id'))
    classroom_schoolyear_id = db.Column(db.String(50),db.ForeignKey('classroom_schoolyears.id'))

    def __init__(self):
        self.id = self

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    student_first = db.Column(db.String(100))
    student_last = db.Column(db.String(100))
    student_full_name = db.Column(db.String(150))
    classes = db.relationship(
        'StudentClasses',
        backref=db.backref('students', lazy=True)
    )

    scores = db.relationship('AssessmentScores', 
                             backref = db.backref('students',lazy=True))

    def __init__(self, id, student_first, student_last, student_full_name):
        self.id = id
        self.student_first = student_first
        self.student_last = student_last
        self.student_full_name = student_full_name


class StudentClasses(db.Model):
    '''Full roster of students for each classroom/schoolyear'''
    #wondering if I should rethink these associations. IRL I'd be connected to an SIS,
    #for this table I made a join in dbeaver between classrooms & students through the assessment table
    #almost wonder if classroom schoolyear and classroom school year period should be an 
    #instance of the classroom class?
    #wrote out logic in thoughts.txt - this might be enough for this project however.
    __tablename__='student_classes'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    class_sy_p_id = db.Column(db.String(50), db.ForeignKey('classroom_schoolyear_periods.id'))
    class_sy_id = db.Column(db.String(50), db.ForeignKey('classroom_schoolyears.id'))

    def __init__ (self, id):
        self.id = self

class Assessment(db.Model):
    '''general information about each assessment'''
    __tablename__='assessment_details'
    id = db.Column(db.String(25),primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)	
    short_name = db.Column(db.String(10), unique = True, nullable = False)	
    family = db.Column(db.String(100))
    type = db.Column(db.String(100))	
    subject = db.Column(db.String(100))	
    content_standard = db.Column(db.String(100))

    def __init__(self, id, name, short_name, family, type, subject, content_standard):
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
    __tablename__ = 'student_assessment_scores'
    id = db.Column(db.String, primary_key=True)
    student_score = db.Column(db.Float(5,2))
    classroom_schoolyear_period_id = db.Column(db.String(100), db.ForeignKey('classroom_schoolyear_period.id'))
    assessment_id = db.Column(db.String(25), db.ForeignKey('assessments.id') )
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, id, student_score, classroom_schoolyear_period_id, assessment_id, student_id):
        self.id = id
        self.student_score = student_score
        self.classroom_schoolyear_period_id = classroom_schoolyear_period_id
        self.assessment_id = assessment_id
        self.student_id = student_id