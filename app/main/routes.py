from models import db, User
from app import login_manager
from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__, template_folder='main_templates')

login_manager.login_view = 'login'


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', username = current_user.username))
    else:
        return render_template('index.html')

#FSQLA: You’ll usually use the Result.scalars() method to get a list of results, 
#or the Result.scalar() method to get a single result.

#from Flask SQL docs:
@main.route('/users')
@login_required
#@admin_required <- not configured yet
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users) #need to make user/list page

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)

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