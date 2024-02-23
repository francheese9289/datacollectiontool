from flask import Blueprint, request, jsonify, render_template
from models import db, User, Staff, Student

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


#this is where data entry pages should go? method = POST

#@api.route('/data_entry', methods = ['POST'])