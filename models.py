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
    role_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, default='Public')
    permissions: so.Mapped[int] = so.mapped_column(sa.Integer)

    #define collection of Staff objects related to each role
    staff_role: so.WriteOnlyMapped['Staff'] = so.relationship(
        back_populates='role_id')

    def __repr__(self):
        return '<Role %r>' % self.permissions

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    #perm for permissions
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
    name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True)
    role_id: so.Mapped[int] =  so.mapped_column(sa.ForeignKey(Role.id)) 
    
    #WriteOnlyMapped defines staff_classrooms as a collection w. Classroom objects inside
    classrooms: so.WriteOnlyMapped['Classroom'] = so.relationship(back_populates='teacher') 
    user: so.WriteOnlyMapped['User'] = so.relationship(back_populates='staff')

    def __repr__(self):
        return f'<Staff Member: {self.staff_name}>'


class User(db.Model, UserMixin):
    '''Creates user accounts and stores user info'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(150), index = True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True, unique=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True, unique=True)
    password_hash = so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    staff_member: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean) #do I need this?
    staff_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Staff.id))

    staff: so.WriteOnlyMapped[Staff] = so.relationship(back_populates='user')
    classrooms: so.WriteOnlyMapped['Classroom'] = so.relationship(back_populates='user_id')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __repr__(self):
        return f'<User: {self.username}>'

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
    
    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    #checks to see if user is staff member when creating an account
    def is_staff_member(self, email):
        staff_member = Staff.query.filter_by(email=email).with_entities(Staff.role_id, Staff.id).first()
        if staff_member:
            staff_id = staff_member.id
            role_id = staff_member.role_id
            staff_user= {'staff_id':staff_id,
                         'role_id': role_id,
                         'staff_member': True}
        else:
            staff_user={'staff_id':0,
                        'role_id':1,
                        'staff_member': False}

        return staff_user
    
   #look at sqla docs, may be an updated version of query and filter


class Classroom(db.Model):
    '''Classroom associates grade level, school and year with their teachers
    to assure student privacy and specificity of access'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    school_year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    school_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    teacher_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Staff.id))
    
    teacher: so.Mapped[Staff] = so.relationship(back_populates='classrooms')
    user_id: so.Mapped[User] = so.mapped_column(sa.Integer, index=True)


class Student(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[int] = so.mapped_column(sa.String(150))
    email: so.Mapped[Optional[int]] = so.mapped_column(sa.String(150))
    #future>include student_users?

    #for student_classes association table
    student_classes: so.WriteOnlyMapped['Classroom'] = so.relationship(
        back_populates='id')

# A common reason to create a table directly is when defining many to many relationships. 
# The association table doesn’t need its own model class, as it will be accessed through the relevant 
# relationship attributes on the related models.

student_classes = sa.Table(
    "student_classes",
    sa.Column('id', sa.Integer, sa.ForeignKey('student.id'),
              primary_key=True),
    sa.Column('id', sa.Integer, sa.ForeignKey('classroom.id'),
              primary_key=True)
)

class AssessmentStandard(db.Model):
    '''general information about each assessment'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    component_id: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True)
    subject: so.Mapped[str] = so.mapped_column(sa.String(50))
    component_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    assessment_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    grade_level: so.Mapped[int] = so.mapped_column(sa.Integer)
    period: so.Mapped[int] = so.mapped_column(sa.Integer)
    rank: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    rank_score: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    score_standard: so.WriteOnlyMapped['AssessmentScore'] = so.relationship(
        back_populates='id')
    

class AssessmentScore(db.Model):
    '''Student assessment scores'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_score: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    
    assessment_id: so.Mapped[int] = so.relationship(sa.ForeignKey(AssessmentStandard.id))
    student_class_id: so.Mapped[int] = so.relationship(sa.ForeignKey(student_classes))
    

    
    #following: so.WriteOnlyMapped['User'] = so.relationship(
    #     secondary=followers, primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     back_populates='followers')
    #followers: so.WriteOnlyMapped['User'] = so.relationship(
    #     secondary=followers, primaryjoin=(followers.c.followed_id == id),
    #     secondaryjoin=(followers.c.follower_id == id),
    #     back_populates='following')

    