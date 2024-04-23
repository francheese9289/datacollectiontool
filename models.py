
import uuid 
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Optional, List
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager() #this is then imported from models > app(init)

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
        back_populates='role_id')
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
        
        for r in roles:
            role = Role.query.get(r)
            if role is None:
                role = Role(role_name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()
   

class Staff(db.Model):
    '''Checks Staff table for new user pre-assigned role, also can update and remove roles '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True)
    role_id: so.Mapped[int] =  so.mapped_column(sa.ForeignKey(Role.id)) 

    #RELATIONSHIPS
    staff_classrooms: so.WriteOnlyMapped[List['Classroom']] = so.relationship() 
    #WriteOnlyMapped defines staff_classrooms as a collection w. Classroom objects inside
    '''Might need to create function for appending classrooms https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-select-relationships'''
    staff_user: so.WriteOnlyMapped['User'] = so.relationship(back_populates='user_staff')

    def __repr__(self):
        return '<Staff Member {}>'.format(self.full_name)
   


class User(db.Model, UserMixin):
    '''Creates user accounts and stores user info'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(150),
                                                index = True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(50),
                                             index=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(150),
                                                  index=True, unique=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(150),
                                                 index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256),
                                                               index=True, unique=True)
    staff_member: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean) #do I need this?
    staff_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(
        Staff.id))
    
    #RELATIONSHIPS
    user_staff: so.WriteOnlyMapped[Staff] = so.relationship(back_populates='staff_user', single_parent=True)
    user_classrooms: so.WriteOnlyMapped[List['Classroom']] = so.relationship(back_populates='user_id')

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

    def set_password_hash(self, password):
        '''password_hash hash- alias of user password_hash to store in db'''
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()
    
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
    
    # def to_dict(self):
    #     '''User data in dict form (from Flask 24 tutorial)'''
    #     data = {
    #         'id': self.id,
    #         'username': self.username,
    #         'email': self.email,
    #         'name': '{}, {}'.format(self.last_name, self.first_name),
    #         'staff_id': self.staff_id,
    #         'links': {'self':'#',
    #                   'classes': '#'}
    #     } #add profile page, class pages, do the same for students and schools
    #     return data

    #def load classrooms?


#Flask tutorial has this outside of class context, need to figure out WHY
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

    
class Classroom(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    school_year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    school_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    teacher_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Staff.id))
    
    #RELATIONSHIPS 
    user_id: so.Mapped[User] = so.relationship(back_populates='user_classrooms')
    class_students: so.WriteOnlyMapped[List['StudentClassroomAssociation']] = so.relationship(
        back_populates='student_class')


    def __repr__(self):
        return '<Classroom {}>'.format(self.id)


class Student(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    email: so.Mapped[Optional[int]] = so.mapped_column(sa.String(150))

    student_classes: so.WriteOnlyMapped[List['StudentClassroomAssociation']] = so.relationship(
        back_populates='class_student')
    student_scores: so.WriteOnlyMapped[List['AssessmentScore']]=so.relationship()

    def __repr__(self):
        return '<Student {}>'.format(self.full_name)

class StudentClassroomAssociation(db.Model):
    '''Association Object connecting Classrooms & Students'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('student.id'))
    classroom_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('classroom.id'))
    
    class_student: so.Mapped['Student'] = so.relationship(back_populates='student_classes')
    student_class: so.Mapped['Classroom'] = so.relationship(back_populates='class_students')
    class_scores: so.Mapped['AssessmentScore'] = so.relationship()
    #each score has one student/class and each student class has a list of scores,
    #connected by foreign key in score table
    # student_class_scores: so.WriteOnlyMapped[List['AssessmentScore']] = so.relationship(back_populates='student_class_id')

    def __repr__(self):
        return '<Student:{}, Class:{}>'.format(self.student_id, self.classroom_id)
    

class AssessmentStandard(db.Model):
    '''general information about each assessment'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    component_id: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True)
    subject: so.Mapped[str] = so.mapped_column(sa.String(50))
    component_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    assessment_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    period: so.Mapped[int] = so.mapped_column(sa.Integer)
    tier: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    tier_benchmark: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    
    standard_scores: so.WriteOnlyMapped[List['AssessmentScore']] = so.relationship()

    def __repr__(self):
        return '<Assessment {}: {}>'.format(self.assessment_name, self.component_name)

class AssessmentScore(db.Model):
    '''Student assessment scores'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_score: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    assessment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(AssessmentStandard.id))
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Student.id)) 
    classroom_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Classroom.id)) 
    

    def __repr__(self):
        return '<Score {}: {}>'.format(self.student_score)
   

    