# #TEMPORARY HOLDING SPOT FOR DB RELATIONSHIPS
# #first migrating the tables, then I'll work on relationships and functions

# #ROLE-------------------------------------------------------------

# #RELATIONSHIPS


# #FUNCTIONS
#     def __repr__(self):
#         return '<Role %r>' % self.permissions

#     def __init__(self,**kwargs):
#         super(Role,self).__init__(**kwargs)
#         if self.permissions is None:
#             self.permissions = 0

#     #perm for permissions
#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm

#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm

#     def reset_permissions(self):
#         self.permissions = 0
    
#     def has_permission(self, perm):
#         return self.permissions & perm == perm
    
#     @staticmethod
#     def insert_roles():
#         roles = {
#             'Public':[Permission.PUBLIC],
#             'Student':[Permission.STUDENT],
#             'Teacher':[Permission.STUDENT, Permission.CLASS],
#             'Principal':[Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.YOY],
#             'Admin':[Permission.STUDENT, Permission.CLASS, Permission.GRADE, Permission.DISTRICT, Permission.YOY]
#         }
        
#         for r in roles:
#             role = Role.query.get(r)
#             if role is None:
#                 role = Role(role_name=r)
#             role.permissions = roles[r]
#             db.session.add(role)
#         db.session.commit()

# #STAFF-------------------------------------------------------------
# # RELATIONSHIPS
    # #WriteOnlyMapped defines staff_classrooms as a collection w. Classroom objects inside
    # classrooms: so.WriteOnlyMapped['Classroom'] = so.relationship(back_populates='teacher') 
    # user: so.WriteOnlyMapped['User'] = so.relationship(back_populates='staff')

# # # FUNCTIONS
#     def __repr__(self):
#         return f'<Staff Member: {self.staff_name}>'

# #USER-------------------------------------------------------------
# # RELATIONSHIPS
# staff: so.WriteOnlyMapped[Staff] = so.relationship(back_populates='user')
    # classrooms: so.WriteOnlyMapped['Classroom'] = so.relationship(back_populates='user_id')

# # # FUNCTIONS
#  def __repr__(self):
#         return '<User {}>'.format(self.username)

#     def __repr__(self):
#         return f'<User: {self.username}>'

#     def create_username(self):
#         print(f'create_username called with first_name: {self.first_name}, last_name: {self.last_name}') 
#         base_username = (self.first_name[0] + self.last_name).lower()
#         username = base_username
#         suffix = 1
#         while User.query.filter_by(username=username).first() is not None:
#             username = f"{base_username}{suffix}"
#             suffix += 1
#         self.username = username
#         return username

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def set_id(self):
#         return str(uuid.uuid4())
    
#     def get_id(self):
#         return str(self.id)
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def set_password_hash(self, password):
#         '''password_hash hash- alias of user password_hash to store in db'''
#         self.password_hash = generate_password_hash(password)

#     def check_password_hash(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     @login_manager.user_loader
#     def load_user(id):
#         return db.session.get(User, int(id))
    
#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return not self.is_authenticated()

#     #checks to see if user is staff member when creating an account
#     def is_staff_member(self, email):
#         staff_member = Staff.query.filter_by(email=email).with_entities(Staff.role_id, Staff.id).first()
#         if staff_member:
#             staff_id = staff_member.id
#             role_id = staff_member.role_id
#             staff_user= {'staff_id':staff_id,
#                          'role_id': role_id,
#                          'staff_member': True}
#         else:
#             staff_user={'staff_id':0,
#                         'role_id':1,
#                         'staff_member': False}

#         return staff_user
    
#    #look at sqla docs, may be an updated version of query and filter

# #CLASSROOM-------------------------------------------------------------
# # # RELATIONSHIPS
#     teacher: so.Mapped[Staff] = so.relationship(back_populates='classrooms')
#     user_id: so.Mapped[User] = so.mapped_column(sa.Integer, index=True)

# # FUNCTIONS

# #STUDENT-------------------------------------------------------------
# # RELATIONSHIPS
    # student_classes: so.WriteOnlyMapped['Classroom'] = so.relationship(
    #     back_populates='id')
# # FUNCTIONS

# student_classes = sa.Table(
#     "student_classes",
#     sa.Column('id', sa.Integer, sa.ForeignKey('student.id'),
#               primary_key=True),
#     sa.Column('id', sa.Integer, sa.ForeignKey('classroom.id'),
#               primary_key=True)
# )

# #ASSESSMENTSTANDARD-------------------------------------------------------------
# # RELATIONSHIPS
    # score_standard: so.WriteOnlyMapped['AssessmentScore'] = so.relationship(
    #     back_populates='id')
# # FUNCTIONS

# #ASSESSMENT SCORES-------------------------------------------------------------
# # # RELATIONSHIPS
#     assessment_id: so.Mapped[int] = so.relationship(sa.ForeignKey(AssessmentStandard.id))
#     student_class_id: so.Mapped[int] = so.relationship(sa.ForeignKey(student_classes))    

# # FUNCTIONS



# example of self referential relationship
    #following: so.WriteOnlyMapped['User'] = so.relationship(
    #     secondary=followers, primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     back_populates='followers')
    #followers: so.WriteOnlyMapped['User'] = so.relationship(
    #     secondary=followers, primaryjoin=(followers.c.followed_id == id),
    #     secondaryjoin=(followers.c.follower_id == id),
    #     back_populates='following')
