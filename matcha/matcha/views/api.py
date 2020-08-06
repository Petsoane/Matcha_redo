from flask import Blueprint, session, request
from matcha import db, logged_in_users, valid_users
from matcha.utils import *

from functools import wraps, cmp_to_key
import html

api = Blueprint('api', __name__)

@api.route('/users/username/search/<username>', methods=['GET', 'POST'])
def search_username(username):
    # global valid_users
    user = db.get_user({'username': username})
    
    return user

