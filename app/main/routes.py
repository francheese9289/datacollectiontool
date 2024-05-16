from models import db, User, login_manager
from forms import UserRegistrationForm
import sqlalchemy as sa
from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__, template_folder='main_templates')

login_manager.login_view = 'auth.login'


@main.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
        return redirect(url_for('main.profile', username=username))
    else:
        return render_template('index.html')


@main.route('/users')
@login_required
#@admin_required <- not configured yet
def user_list():
    users = db.session.execute(sa.select(User).order_by(User.last_name)).scalars()
    return render_template("user/list.html", users=users)
#TO DO: make admin page


@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    '''
    Generate profile page for each user.
    '''
    user=db.first_or_404(sa.select(User).where(User.username == username))
    user_data = user.to_dict()
    class_data = user.get_current_classroom()
    return render_template('profile.html', user=user, user_data=user_data, class_data=class_data)

@main.route('/edit_profile/<username>', methods=['GET', 'POST'])
#testing to see how to make populate_obj work for editing data
@login_required
def edit_profile(username):
    user = current_user
    form = UserRegistrationForm()
    if request.method == 'POST' and form.validate():
        #I'd like to better understand how POST, GET etc. work in flask
        form.populate_obj(user) #should overwrite the user's data with the form data
        db.session.save(user)
        db.session.commit() 
        return redirect(url_for('edit_profile', username=username))
    return render_template('edit_profile.html', user=user, form=form)
