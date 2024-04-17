from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import uuid 
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()
login_manager = LoginManager()

###To insepect database tables use: psql postgresql://vydvbwqr:stgmpejxJhNPWLBWa9PL5JO39puT7k2H@salt.db.elephantsql.com/vydvbwqr
##Can use SQL queries during inspection \dt \d \q

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
    role_name = db.Column(db.String(150), default ='User')
    permissions = db.Column(db.Integer)

    # staff = db.relationship('Staff', back_populates='staff.role')

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
            'Student':[Permission.STUDENT],
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
    staff_name = db.Column(db.String(150))
    staff_email = db.Column(db.String(319), unique=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #back ref for users > staff members
    staff_user = db.relationship('User', back_populates='staff_id')

    #back ref for classrooms > staff members
    classrooms = db.relationship('Classroom', back_populate='teacher_id', lazy='dynamic')

    def __init__(self, staff_id, staff_name, staff_email, role):
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.staff_email = staff_email
        self.role = role
    
    def __repr__(self):
        return f'<Staff Member: {self.staff_name}>'



class User(db.Model, UserMixin):
    '''Creates user accounts and stores user info'''
    __tablename__ ='users'

    user_id = db.Column(db.String, primary_key=True)
    user_email = db.Column(db.String(50), nullable = False)
    user_first_name = db.Column(db.String(150), nullable=True, default='')
    user_last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), unique = True, nullable = False)
    user_password = db.Column(db.String, nullable = True, default = '')
    staff_member = db.Column(db.Boolean, default = False)

    staff_id = db.relationship('Staff', back_populates = 'staff_user')

    #back ref for users > classrooms
    user_classrooms = db.relationship('Classroom', backref='user_id', lazy='dynamic')
    # user_role = db.relationship('Staff', back_populates = 'user_id')
    # primaryjoin ="and_(Staff.staff_id == foreign(User.staff_id),""Staff.role == User.user_role)

    def __init__(self, user_email, user_first_name, user_last_name, user_password):
        print(f'Init called with email: {user_email}, first_name: {user_first_name}, last_name: {user_last_name}') 
        
        self.user_id = self.set_id()
        self.user_email = user_email
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name

        print(f'Before create_username: {self.user_first_name}, {self.user_last_name}') 
        self.user_password = self.set_password(user_password) if user_password else ''
        self.username = self.create_username()

        print(f'After create_username: {self.username}')
        user_staff_info = self.is_staff_member(user_email)
        self.staff_id = user_staff_info['staff_id']
        self.staff_member = user_staff_info['staff_member']

    def __repr__(self):
        return f'<User: {self.username}>'

    def create_username(self):
        print(f'create_username called with first_name: {self.user_first_name}, last_name: {self.user_last_name}') 
        base_username = (self.user_first_name[0] + self.user_last_name).lower()
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
        staff_member = Staff.query.filter_by(email=email).with_entities(Staff.role, Staff.staff_id).first()
        if staff_member:
            staff_id = staff_member.staff_id
            role_id = staff_member.role
            user_staff= {'staff_id':staff_id,
                         'role_id': role_id,
                         'staff_member': True}
        else:
            user_staff={'staff_id':0,
                        'role_id':1,
                        'staff_member': False}

        return user_staff


class Classroom(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    __tablename__ = 'classrooms'
    #CHILD CLASS to staff
    classroom_id = db.Column(db.String(150), primary_key=True)
    school_year = db.Column(db.Integer)
    school_name = db.Column(db.String(150))
    teacher_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id')) 
    user_id = db.Column(db.Integer, db.ForeignKey ('user.user_id'))

    #for student_classes association table
    staff = db.relationship('Staff', back_populates='classrooms')
    
    def __init__(self, classroom_id, school_year, school_name, teacher_id, user_id):
        self.classroom_id = classroom_id
        self.school_year = school_year
        self.school_name = school_name
        self.teacher_id = teacher_id
        self.user_id = user_id

class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key = True)
    student_name = db.Column(db.String(150))
    student_email = db.Column(db.String(150))
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #for student_classes association table
    student_classes = db.relationship('StudentClass', back_populates='student_id', lazy='dynamic')
    
    def __init__(self, student_id, student_name, student_email, role):
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.role = role

class StudentClass(db.Model):
    '''Association table for students and classrooms'''
    __tablename__='student_classes'
    student_class_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.student_id'))
    classroom_id = db.Column(db.String(150), db.ForeignKey('classrooms.classroom_id'))

    student_class_scores = db.relationship('AssessmentScore', back_populates='student_class_id', lazy='dynamic')

    def __init__ (self, student_class_id):
        self.student_class_id = student_class_id

    #def add_new_classes(): naming convention

class AssessmentStandard(db.Model):
    '''general information about each assessment'''
    __tablename__='assessment_standards'
    standard_id = db.Column(db.Integer, primary_key = True)
    component_id = db.Column(db.String(10))
    subject = db.Column(db.String(50))	
    component_name = db.Column(db.String(50))	
    assessment_name = db.Column(db.String(150))	
    grade_level = db.Column(db.Integer)
    period = db.Column(db.Integer)
    rank_name = db.Column(db.String(10))
    rank_score = db.Column(db.Integer)

    assessment_standard_scores = db.relationship('AssessmentScore', back_populates='standard_id', lazy='dynamic')

    def __init__(self, standard_id, component_id, subject, component_name, assessment_name, grade_level, period, rank_name, rank_score):
        self.standard_id = standard_id
        self.component_id = component_id
        self.subject = subject
        self.component_name = component_name
        self.assesment_name = assessment_name
        self.grade_level = grade_level
        self.period = period
        self.rank_name = rank_name
        self.rank_score = rank_score


class AssessmentScore(db.Model):
    '''Student assessment scores'''
    __tablename__ = 'assessment_scores'
    assessment_score_id = db.Column(db.String, primary_key=True)
    student_score = db.Column(db.Integer)
    standard_id = db.Column(db.String(50), db.ForeignKey('assessment_standards.standard_id') )
    student_class_id = db.Column(db.Integer, db.ForeignKey('student_classes.student_class_id'))
    

    def __init__(self, assessment_score_id, student_score, standard_id, student_class_id):
        self.assessment_score_id = assessment_score_id
        self.student_score = student_score
        self.standard_id = standard_id
        self.student_class_id = student_class_id