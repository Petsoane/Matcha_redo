from flask import Blueprint, render_template, session, redirect, flash, request, url_for
from matcha import db, valid_users, logged_in_users
from functools import wraps, cmp_to_key
import html

from matcha.utils import login_required, finish_profile

main = Blueprint('main', __name__)

test_user = 'Lebogang'

@main.route('/')
@login_required
@finish_profile
def home():
    posts = (db.get_posts())
    user = db.get_user({'username': test_user})

    # get notifications and merge them to the dictionary
    notifications = db.get_notifications(user['id']) # Does the fetchall function get all
    if isinstance(notifications, tuple):
        notifications = {}

    user['notifications'] = notifications
    for post in posts:
        for key, value in post.items():
            if key == 'author':
                post[key] = db.get_user({'id': post[key]})
            if key == 'title' or key == 'content':
                post[key] = html.unescape(value)

    print('posts', posts)
    return render_template('home.html', logged_in_user='Lebo', posts=posts, current_user=user)
    # return posts[0]


@main.route('/users')
def users():
    # Get the logged in user
    user = db.get_user({'username': test_user})
    print(user)
    # Get the users blocked lisg

    # Filter out all the users that dont match the sexual preference.

    # Filter out the users in the blocked list. ! This can be done in the backend.. maybe?

    # Assign to the valid users global variable.

    # render the page
    return 'This is the user page'
