'''Helps with other functions, including making sure users
can login correctly and have access to the right API data
FOR MY PROJECT I'll need classroom, school and district level views'''
from functools import wraps
from flask import request, jsonify, json
import decimal
from .models import User, UserClassroom, Permission, SchoolYear, ClassroomSchoolYear, db
from datetime import datetime

def current_year():
    year = datetime.now().year
    return year

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)





    # Assign schools if the user is a principal



