
import uuid 
import sqlalchemy.orm as so
import sqlalchemy as sa
import pandas as pd
from typing import Optional, List
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
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

#SQLAlchemy automatically defines an __init__ method for each model that assigns 
#any keyword arguments to corresponding database columns and other attributes.

class Role(db.Model):
    '''Associate permissions with roles, add and remove permissions from roles'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, default='Public')
    permissions: so.Mapped[int] = so.mapped_column(sa.Integer)

    #RELATIONSHIPS
    staff_role: so.WriteOnlyMapped['Staff'] = so.relationship(
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    # student_role: so.WriteOnlyMapped['Student'] = so.relationship()
    #WriteOnlyMapped defines collection of Staff objects related to each role
    
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
            'Public':[Permission.PUBLIC],
            'Student':[Permission.STUDENT],
            'Teacher':[Permission.STUDENT, Permission.CLASS],
            'Principal':[Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.YOY],
            'Admin':[Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.DISTRICT, Permission.YOY]
        }
        
        for role_name, permissions in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
            role.permissions = sum(permissions)
            db.session.add(role)
        db.session.commit()

class Staff(db.Model):
    '''Checks Staff table for new user pre-assigned role, also can update and remove roles '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True)
    profile: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), unique=True)
    role_id: so.Mapped[int] =  so.mapped_column(sa.ForeignKey(Role.id, ondelete="cascade")) 

    staff_classrooms: so.Mapped[List['Classroom']] = so.relationship(
        passive_deletes=True, order_by='Classroom.school_year'
    ) 

    def __repr__(self):
        return '<Staff Member {}>'.format(self.full_name)
    
    def staff_profile(self):
        #Moved this function from User to Staff, so that all staff have a profile, regardless if they have an account.
        first_last = self.full_name.split( )
        base_username = (first_last[0][0] + first_last[-1]).lower()
        username = base_username
        suffix = 1
        while Staff.query.filter_by(username=username).first() is not None:
            username = f"{base_username}{suffix}"
            suffix += 1
        self.username = username
        return username
    
    def profile_to_dict(self):
        '''info to display on profile'''
        current_classroom = self.staff_classrooms[-1]
        #not worrying about the year right, just using most recent classroom
        data = current_classroom.to_dict()
        return data 

        
class User(db.Model, UserMixin):
    '''Creates user accounts and stores user info'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(150))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(150))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    username: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), unique=True)
    staff_member: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean) #do I need this?
    staff_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Staff.id))
    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        '''password_hash - alias of user password to store in db'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    def user_profile(self):
        base_username = (self.first_name[0].lower() + self.last_name.lower())
        username = base_username
        suffix = 1
        while User.query.filter_by(username=username).first() is not None:
            username = f"{base_username}{suffix}"
            suffix += 1
        self.username = username
        return self.username

    def to_dict(self):
        '''User data in dict form (from Flask 24 tutorial)'''
        
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': '{} {}'.format(self.first_name, self.last_name),
        } 
        return data
    #add profile page, class pages, do the same for students and schools
    # read tutorial for how to use url for

    def get_current_classroom(self):
        '''Returns the most recent classroom for a user'''
        if self.staff_member:
            staff = db.session.scalar(sa.select(
        Staff).where(Staff.id == self.staff_id))
            return staff.staff_classrooms[-1]
        else:
            return None


class Classroom(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    school_year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    school_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    teacher_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Staff.id))
    
    #RELATIONSHIPS 
    class_students: so.Mapped[List['StudentClassroomAssociation']] = so.relationship(
        back_populates='student_class',
        passive_deletes=True,
        order_by='StudentClassroomAssociation.classroom_id')
    class_scores: so.Mapped[Optional[List['AssessmentScore']]] = so.relationship()


    def __repr__(self):
        if self.grade_level == 0:
            return (
                f'{self.school_year} | {self.school_name} | Kindergarten'
            )
        else:
            return (
                f'{self.school_year} | {self.school_name} | Grade {self.grade_level}'
            )
    
    def to_dict(self):
        teacher_name = db.session.scalar(sa.select(
            Staff.full_name).where(
                Staff.id == self.teacher_id)) #for some reason this isn't working properly, giving wrong name
        if self.grade_level == 0:
            data = {
                'school_year': self.school_year,
                'school_name': self.school_name,
                'grade_level': 'Kindergarten',
                'teacher': teacher_name
            }
        else:
            data = {
                'school_year': self.school_year,
                'school_name': self.school_name,
                'grade_level': f'Grade {self.grade_level}',
                'teacher': teacher_name
            }
        return data
    
    def classroom_roster(self):
        classroom_roster = []
        students = self.class_students
        for student in students:
            class_student = {
                'student_id': student.class_student.id,
                'student_name':student.class_student.full_name}
            classroom_roster.append(class_student)
        return classroom_roster
    

class Student(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    email: so.Mapped[Optional[int]] = so.mapped_column(sa.String(150))
    profile: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), unique=True)

    student_classes: so.WriteOnlyMapped[List['StudentClassroomAssociation']] = so.relationship(
        back_populates='class_student')
    student_scores: so.WriteOnlyMapped[List['AssessmentScore']]=so.relationship()

    def __repr__(self):
        return '<Student {}>'.format(self.full_name)
    
    def student_profile(self):
        first_last = self.full_name.split( )
        base_username = (first_last[0][0] + first_last[-1]).lower()
        username = base_username
        suffix = 1
        while Student.query.filter_by(username=username).first() is not None:
            username = f"{base_username}{suffix}"
            suffix += 1
        self.username = username
        return username
    
    def to_dict(self):
        current_classroom = self.student_classes[-1]
        cc_data = current_classroom.to_dict()
        data = {
            'name': self.full_name,
            'school': cc_data['school_name'],
            'grade_level': cc_data['grade_level'],
            'teacher': cc_data['teacher_name']
        }

    def student_score_df(self):
        '''
        Merges student dict with score dict and
        returns a detailed dataframe.
        '''
        student_scores = []
        scores = self.student_scores
        for score in scores:
            student_score_dict = score.to_dict()
            student_scores.append(student_score_dict)
        full_score_data = pd.DataFrame(student_scores)
        return full_score_data

class StudentClassroomAssociation(db.Model):
    '''Association Object connecting Classrooms & Students'''
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('student.id'), primary_key=True)
    classroom_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey('classroom.id'), primary_key=True)

    class_student: so.Mapped['Student'] = so.relationship(back_populates='student_classes')
    student_class: so.Mapped['Classroom'] = so.relationship(back_populates='class_students')
    

    def __repr__(self):
        return '<Student:{}, Class:{}>'.format(self.student_id, self.classroom_id)

    def classroom_roster_dict(self):
        students = []
        for student_id in self.class_student.id:
            students.append(Student.query.filter_by(id=student_id).first().full_name)
        data = {
            'classroom_id': self.classroom_id,
            'students': students
        }    
        return data
    
class AssessmentComponent(db.Model):
    '''New table for assessment components, separate from assessment standards'''
    id: so.Mapped[str] = so.mapped_column(primary_key=True)
    subject: so.Mapped[str] = so.mapped_column(sa.String(50))
    component_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    assessment_name: so.Mapped[str] = so.mapped_column(sa.String(100))

    component_standards: so.Mapped[List['AssessmentStandard']] = so.relationship()
    component_scores: so.Mapped[List['AssessmentScore']] = so.relationship()

    def __repr__(self):
        return '<{}: {}>'.format(self.assessment_name, self.component_name)

    def to_dict(self):
        data ={
            'id': self.id,
            'assessment_name': self.assessment_name,
            'component_name': self.component_name,
            'subject': self.subject
        }
        return data

class AssessmentScore(db.Model):
    '''Student assessment scores'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_score: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    period: so.Mapped[int] = so.mapped_column(sa.Integer)
    score_tier: so.Mapped[Optional[str]] = so.mapped_column(sa.String) #remove this?
    component_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(AssessmentComponent.id))
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Student.id)) 
    classroom_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Classroom.id))
    
    def __repr__(self):
        return '<Score {}>'.format(self.student_score)
    



class AssessmentStandard(db.Model):
    '''general information about each assessment'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    component_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(AssessmentComponent.id))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    period: so.Mapped[int] = so.mapped_column(sa.Integer)
    tier_1: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    tier_2: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    tier_3: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    standard_components: so.Mapped[List['AssessmentComponent']] = so.relationship(back_populates='component_standards')

    def __repr__(self):
        return '<Standard for {}, Grade {}, Period {}, {}: {}>'.format(self.component_id, self.grade_level, self.period, self.tier, self.tier_benchmark)
    
    def to_dict(self):
        data = {
            'component_id': self.component_id,
            'grade_level': self.grade_level,
            'period': self.period,
            'tier_1': self.tier_1,
            'tier_2': self.tier_2,
            'tier_3': self.tier_3,
        }
        return data 