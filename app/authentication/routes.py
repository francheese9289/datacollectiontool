from forms import UserSignUpForm, CheckUserForm
from models import User, db, Staff
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_httpauth  import HTTPTokenAuth, HTTPBasicAuth #flask login replacement


auth = Blueprint('auth', __name__, template_folder='auth_templates')

basic_auth = HTTPBasicAuth() #ONLY TAKES USERNAME AND PASSWORD ARGUMENTS 
token_auth = HTTPTokenAuth()

@auth.route('/signin', methods = ['GET', 'POST'])
@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
    if user is not None and user.check_password(password):
        return user
    return None

@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    '''Sign up form to create new users'''
    form = CheckUserForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            staff_member = db.session.execute(db.select(Staff).where(Staff.email == form.email)).first()
            if staff_member:
                for attribute in staff_member.scalars():
                    flash (f'Email recognized, welcome {attribute.first_name}!')
                    new_user = User(
                        role= attribute.role,
                        first_name = attribute.first_name,
                        last_name = attribute.last_name,  
                    )
                return redirect(url_for('site.home'))
            else:
                user_email = form.email.data
                form = UserSignUpForm
                new_user = User(
                    email = user_email,
                    role_id = 1,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data, 
                    password = form.password.data
                    )
        db.session.add(new_user)
        db.session.commit()
        flash (f'You have successfully created a user account {form.email}', 'User-created')
        return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')


# @basic_auth.login_required
# def handle_error(status):
#     return {"error":"Incorrect username/password, please try again!"}, status

# @auth.route('/classroom_data/<classroom_id>')
# @auth.login_required(role=['Teacher','Principal','Administrator'])
# def follow_classroom(classroom_schoolyear_id):
#     if User.follow_classrooms(classroom_schoolyear_id):
#         classroom_data = get_classroom_data(classroom_schoolyear_id)
#         return render_template ('classroom_page.html', data=classroom_data)


# @auth.route('/school/<int:school_id>')
# @permission_required
# def view_school(school_id):
#     if User.follow_school(school_id):
#         school_data = get_school_data(school_id)  # Function to fetch school data
#         return render_template('school_page.html', data=school_data)
#     else:
#         return "You are not authorized to view this school's data.", 403


# @basic_auth.get_user_roles
# def get_user_roles(user):
#     return user.get_roles()
# @auth.route('/admin')
# @auth.login_required(role='admin')
# def admins_only():
#     return "Hello, {}".format(auth.current_user())