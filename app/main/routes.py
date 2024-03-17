from flask import Blueprint, render_template, flash, redirect, url_for, request, flash, session, abort
from flask_login import login_required, current_user
from models import db, User, Student, AssessmentScores, login_manager
import pandas as pd
from db_util import *

main = Blueprint('main', __name__, template_folder='main_templates')

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', username = current_user.username))
    return render_template('index.html')


@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    if username != current_user.username:
        abort(403)  

    user_classes = fetch_all_classes(current_user.staff_id)
    # rosters_by_class = group_rosters_by_class(rosters)
    profile_url = url_for('main.profile', username = current_user.username)
    return render_template('profile.html', user_classes=user_classes, profile_url = profile_url)
