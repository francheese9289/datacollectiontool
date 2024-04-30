from models import db, User, Classroom
from app import login_manager
from forms import UserRegistrationForm
import sqlalchemy as sa
from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__, template_folder='main_templates')

login_manager.login_view = 'login'


@main.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.get_username()
        return redirect(url_for('main.user_profile', username=username))
    else:
        return render_template('index.html')

#FSQLA: You’ll usually use the Result.scalars() method to get a list of results, 
#or the Result.scalar() method to get a single result.

#from Flask SQL docs:
@main.route('/users')
@login_required
#@admin_required <- not configured yet
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.html", users=users) #need to make user/list page


@main.route('/user_profile/<username>', methods=['GET'])
@login_required
def user_profile(username):
     '''
     Generate url end point by fetching logged in user's username.
     '''
     username = current_user.get_username()
     user_data = current_user.to_dict()
     
     return render_template('user_profile.html', username=username, user_data=user_data)

@main.route('/edit_user_profile/<user>', methods=['GET', 'POST'])
#testing to see how to make populate_obj work for editing data
@login_required
def edit_user_profile(user):
     user= current_user
     form = UserRegistrationForm()
     if request.method == 'POST' and form.validate():
         form.populate_obj(user)
         db.session.save(user)
         db.session.commit()
         redirect ('edit_user_profile')
     return render_template('edit_user_profile.html', user=user, form=form)
