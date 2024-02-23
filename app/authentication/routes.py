from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from models import User, db, login_manager, check_password_hash
from forms import UserRegistrationForm, UserLoginForm
# from flask_httpauth  import HTTPTokenAuth, HTTPBasicAuth
# imports for flask login 
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''User Login Form'''
    form = UserLoginForm()
    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
                return render_template('login.html', form=form)
    except:
        flash('You do not have access to this content','auth-failed')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    try:
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                user = User(
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data  
                )
                # set staff_member and role_id
                user.staff_member = user.is_staff_member()
                user.role_id = user.get_role_id()

                #add user to database
                db.session.add(user)
                db.session.commit()

                #success message
                flash(f'Account created for {user.email}!', 'success')
                return redirect(url_for('main.profile'))
            else:
                #duplicate account
                flash('Email already exists, please login.', 'danger')
                return redirect(url_for('auth.login'))
    except Exception as e:
        flash(f'Error during registration: {e}', 'danger')
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('main'))



# basic_auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth()

# @basic_auth.verify_password
# def verify_password(email, password):
#     if email in User.query.filter_by(emaile=User.email) and User.check_password(User.get(email), password):
#         return email
# @basic_auth.login_required
# def authenticate_user(username, password):

#     for user in User.query.values():
#         if user.username == username and verify_password(user, password):
#             return user
#     return None

# @basic_auth.login_required
# def handle_error(status):
#     return {"error":"Incorrect username/password, please try again!"}, status

    