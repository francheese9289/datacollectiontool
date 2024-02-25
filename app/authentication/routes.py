from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from models import User, db, login_manager, check_password_hash
from forms import UserRegistrationForm, UserLoginForm
# from flask_httpauth  import HTTPTokenAuth, HTTPBasicAuth
# imports for flask login 
from flask_login import login_user, logout_user, login_required
from email_validator import validate_email


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view='login'

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''User Login Form'''
    form = UserLoginForm()
    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
       
            user = User.query.filter(User.email == email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
                return render_template('login.html', form=form)
    except:
        flash('You do not have access to this content','auth-failed')
    return render_template('login.html', form=form)



@auth.route('/register', methods=['GET','POST'])
def register():
    print("Start of registration route")  
    form = UserRegistrationForm()
    try:
        if form.validate_on_submit():
            print("Form is valid")
            print(f'First Name: {form.first_name.data}, Last Name: {form.last_name.data}') 
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                print("Creating new user") 
                user = User(
                    email= form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data
                )

                user.set_id()
                user.create_username()
                user_staff_info = user.is_staff_member(email=form.email.data)
                user.set_password(form.password.data)

                print(f'User instance: {user}') 


                db.session.add(user)
                db.session.commit()

                login_user(user)

                #success message
                flash(f'Account created for {user.email}!', 'success')
                print("before redirect")
                return redirect(url_for('main.profile'))
            else:
                #duplicate account
                print("Email already exists") 
                flash('Email already exists, please login.', 'danger')
                return redirect(url_for('auth.login'))
        else:
           print(form.errors)
    except Exception as e:
        print(f'Error during registration: {str(e)}')
        flash(f'Error during registration: {e}', 'danger')
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('main.index'))

    