from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session, abort, jsonify
from flask_login import login_required, current_user
from models import db, User
from queries import *

main = Blueprint('main', __name__, template_folder='main_templates')

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', username = current_user.username))
    else:
        return render_template('index.html')


@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
     '''
     Generate url end point by fetching logged in user's username.
     Populate profile with user/teacher's classrooms. 
     '''
     profile = User.query.filter_by(username=username).first()
     user_classes = Classroom.query.filter_by(teacher_id=current_user.staff_id).all()
    #  user_classrooms = current_user.follow_classrooms() 
     
     return render_template('profile.html', profile=profile, user_classrooms=user_classes)