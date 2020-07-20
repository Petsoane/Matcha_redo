from flask import Blueprint, render_template, session, redirect, flash, request, url_for
from matcha import db

from functools import wraps
import secrets, re, bcrypt, html
from datetime import datetime 

# Create a blueprint
auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
	errors = []
	details = {
		'username': '',
		'firstname': '',
		'lastname':'',
		'age': 0,
		'password':'',
		'email': '',
	}

	if request.method == 'POST':
		print("-------------------------------------",request.form.get("username"))
		details['username'] = html.escape(request.form.get('username')) 
		details['firstname'] = html.escape(request.form.get("firstname"))
		details['lastname'] = html.escape(request.form.get('lastname'))
		details['email'] = html.escape(request.form.get('email'))
		details['password'] = html.escape(request.form.get('password'))
		passwd_confirm = html.escape(request.form.get('password_confirm'))

		# check users username
		if not details['username']:
			errors.append('The username cannot be empty')
		if not re.match('^[A-Za-z][A-Za-z0-9]{2,49}$', details['username']):
			errors.append('The username must be alpha numeric value begining with a letter')
		# if db.get_user({'username': details['username']}):
		# 	errors.append('The username is already take.')

		# Check the users email
		if db.get_user({'email': details['email']}):
			errors.append('the email is already taken!')
		if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,100}$', details['email']):
			errors.append('invalid email format')
		
		# Check the users password
		if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{5,25}$", details['password']):
			errors.append("the password is invalid")
		if passwd_confirm != details['password']:
			errors.append('Confirmation password is invalid')

		# Check the users firstname

		# check the users age

		# Check the users lastname

		if not errors:
			salt = bcrypt.gensalt()
			details['password'] = bcrypt.hashpw(details['password'].encode('utf-8'), salt)
			db.register_user(details)

			return 'check database'

			
	return '\n'.join(errors)


