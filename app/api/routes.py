'''my api enabled routes and views'''
from flask import Blueprint, request, jsonify


api = Blueprint('api',__name__, url_prefix='/api')

# @api.route('/classroom', methods = ['GET'])
# def my_classroom (current_user_token):
#     a_user = current_user_token.token
#     students = Student.query.filter_by(user_token=a_user).all() #display students in classrooms
#     #need to make STUDENT to see student names  and finish this function

