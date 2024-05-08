import sqlalchemy as sa
from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import User, Staff, Student, Classroom, StudentClassroomAssociation, AssessmentStandard, AssessmentScore, db
from flask_login import current_user
from forms import AssessmentScoreForm

data = Blueprint('data', __name__, template_folder='data_templates')

#data/routes.py