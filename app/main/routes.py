from models import db, User, Classroom, login_manager, Staff
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
        return redirect(url_for('main.user', username=username))
    else:
        return render_template('index.html')


@main.route('/users')
@login_required
#@admin_required <- not configured yet
def user_list():
    users = db.session.execute(sa.select(User).order_by(User.last_name)).scalars()
    return render_template("user/list.html", users=users) #need to make user/list page


@main.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    '''
    Generate url end point by fetching logged in user's id.
    '''
    user=db.first_or_404(sa.select(User).where(User.username == username))
    user_data = user.to_dict()
    staff = db.session.scalar(sa.select(Staff).where(Staff.id == user.staff_id))
    class_data = staff.staff_classrooms[-1]
    return render_template('user.html', user=user, user_data=user_data, class_data=class_data)

@main.route('/edit_user/<username>', methods=['GET', 'POST'])
#testing to see how to make populate_obj work for editing data
@login_required
def edit_user(username):
    user=db.first_or_404(sa.select(User).where(User.username == username))
    form = UserRegistrationForm()
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        db.session.save(user)
        db.session.commit()
        redirect ('edit_user')
    return render_template('edit_user.html', user=user, form=form)
