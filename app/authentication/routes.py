import sqlalchemy as sa
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from werkzeug.middleware.profiler import ProfilerMiddleware
from wtforms.validators import ValidationError
from models import User, Staff, db, login_manager
from forms import UserRegistrationForm, UserLoginForm
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login user by validating login form (email & password).
    Redirect to profile page if/once logged in.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.user', username=current_user.username))
    
    form = UserLoginForm()
    if form.validate_on_submit():
        #create instance of User class, find user by email address
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))

        #validate user's password 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        

        flash('Login successful!', 'success')
        
        return redirect(url_for('main.profile', username=user.username))
    
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        staff = db.session.scalar(sa.select(Staff).where(
            Staff.email == form.email.data
            ))
        existing_user = db.session.scalar(sa.select(User).where(
            User.email == form.email.data))
        if staff is None:
            raise ValidationError('Email not recognized, please use an organization email address.')
        elif existing_user is not None:
            flash ('Email already exists, please login.')
            return redirect(url_for('auth.login'))
        else:
            print("Creating new user") 
            user = User(
                email= form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )

            user.set_id()
            user.set_password(form.password.data)
            user.user_profile()
            user.staff_member = True
            user.staff_id = staff.id
            

            print(f'User instance: {user}') 

            db.session.add(user)
            db.session.commit()

            login_user(user)

            #success message
            flash(f'Account created for {user.email}!', 'success')
            return redirect(url_for('main.profile', username=user.username))
    else:
        return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('main.index'))

    