from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import uuid 
import sqlalchemy.orm as so
# from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import sqlalchemy as sa

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

    #<Relationships>
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

    def __repr__(self):
        return '<User {}>'.format(self.username)
   


class Classroom(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    school_year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    school_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    teacher_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Staff.id))
    
    def __repr__(self):
        return '<Clasroom {}>'.format(self.id)

class Student(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    email: so.Mapped[Optional[int]] = so.mapped_column(sa.String(150))

    def __repr__(self):
        return '<Student {}>'.format(self.full_name)

# A common reason to create a table directly is when defining many to many relationships. 
# The association table doesn’t need its own model class, as it will be accessed through the relevant 
# relationship attributes on the related models.



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

    def __repr__(self):
        return '<Assessment {}: {}>'.format(self.assessment_name, self.component_name)

class AssessmentScore(db.Model):
    '''Student assessment scores'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_score: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    
    
    def __repr__(self):
        return '<Score {}: {}>'.format(self.student_score)
   

    