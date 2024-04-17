from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from models import User, db, login_manager, check_password_hash
from forms import UserRegistrationForm, UserLoginForm
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login user by validating login form (email & password).
    Redirect to profile page if/once logged in.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    #login from
    form = UserLoginForm()
    if form.validate_on_submit():
        #create instance of User class, find user by email address
        user = db.session.scalar(User.query.filter_by(User.email == form.email.data))

        #validate user's password 
        if user and check_password_hash(user.password, form.password.data):

            #login user
            login_user(user, remember=True)
            flash('Login successful!', 'success')

            username = user.username
            return redirect(url_for('main.profile', username=username))
        
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('login.html', form=form)

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
                username = user.create_username()
                user_staff_info = user.is_staff_member(email=form.email.data)
                user.set_password(form.password.data)

                print(f'User instance: {user}') 


                db.session.add(user)
                db.session.commit()

                login_user(user)

                #success message
                flash(f'Account created for {user.email}!', 'success')
                print("before redirect")
                return redirect(url_for('main.profile', username=username))
            else:
                #duplicate account message
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

    