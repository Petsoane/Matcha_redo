from flask import Blueprint, render_template, session, redirect, flash, request, url_for
from matcha import db, logged_in_users
from matcha.utils import *

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
		# if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{5,25}$", details['password']):
		# 	errors.append("the password is invalid")
		# if passwd_confirm != details['password']:
		# 	errors.append('Confirmation password is invalid')

		# Check the users firstname
		if not re.match('^[A-Z][a-zA-Z-]{1,24}$', details['firstname']):
			errors.append('A name must start with a capital letter.')
		
		# check the users age
		try:
			details['age'] = int(request.form.get('age'))
			if  details['age'] < 18 or details['age'] > 100:
				errors.append('Age needs to be a number')
		except ValueError:
			errors.append("Age needs to be a number")

		# Check the users lastname
		if not re.match('^[A-Z][ a-zA-Z-]{1,24}$', details['lastname']):
			errors.append("The lastname must start with a capital letter.")
		

		if not errors:
			salt = bcrypt.gensalt()
			details['password'] = bcrypt.hashpw(details['password'].encode('utf-8'), salt)
			db.register_user(details)

			flash("Please check your mail for confirmation", "success")
			# this should return a redirect to the correct page.
			return redirect( url_for('auth.login') )
		
		# Flash errors
		for error in errors:
			flash(error,'danger')
		
	# This should render the template.
	return render_template('auth/register.html', details=details)

@auth.route('/confirm', methods=['GET'])
def confirm():
	errors = []
	if request.method == 'GET':
		jrr = request.args.get('jrr')

		user = db.get_user({'_id': jrr})
		print('[ user stuff ]', user)
		if user:
			# update flirts
			pass
		else:
			errors.append('Incorrect username or password')
			# flash errors to the screen

	return '\n'.join(errors)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	errors = []
	details = {
		'username': '',
		'password': ''
	}

	if request.method == 'POST':
		details['username'] = html.escape(request.form.get('username'))
		details['password'] = html.escape(request.form.get('password'))
		details['password'] = details['password'].encode('utf-8')

		user = db.get_user({'username': details['username']})

		# print(details["email_confirmed"])

		if not user:
			errors.append('Incorrect username or password')
		# elif not bool(user['email_confirmed']):
		# 	errors.append('Please check your email for confirmation')

		user['password'] = user['password'].encode('utf-8')
		if not bcrypt.checkpw(details['password'], user['password']):
			errors.append('Incorrect username or password')


		if not errors:
			session['username'] = details['username']
			flash('Successful login', 'success')
			if not details['username'] in logged_in_users:
				logged_in_users[details['username']] = ''
			
			calculate_fame(user)
			return redirect( url_for('main.home') )

		# flash errors
		for error in errors:
			flash(error, 'danger')

	return render_template("auth/login.html", details=details)
	# return '\n'.join(errors)

@auth.route('/logout')
def logout():
	user = db.get_user({'username': session.get('username')})

	user['last-seen'] = datetime.utcnow()
	db.update_user(user)

	# logged_in_users.pop(session.pop('username'), None)

	return "the use is logged out"

@auth.route('/forgotpw', methods=['GET','POST'])
def forgotpw():
	errors = []
	details = {}

	if request.method == 'POST':
		username = request.form.get('username')
		user = db.get_user({'username': username})

		if not username:
			errors.append('The username cannot be empty')
		if not re.match('^[A-Za-z][A-Za-z0-9]{2,49}$', username):
			errors.append('Invalid username')
		if not user:
			errors.append('No such user found, please register an account, peasant')

		if not errors:
			flash('Please check your email to reset your password', 'success')

		# Flash errors
		for error in errors:
			flash(error,'danger')
		
	return render_template('auth/forgotpw.html', details=details)


@auth.route('/resetpw', methods=['GET','POST'])
def resetpw():
	errors = []

	if request.method == 'GET':
		jrr = request.args.get('jrr')
	
	if request.method == 'POST':
		jrr = request.args.get('jrr')
		user = db.get_user({'id': jrr})
		password = request.form.get('password')
		password_repeat = request.form.get('password_confirm')

		if not re.match('[A-Za-z0-9]', password):
			errors.append('The password must have an uppcase, lowercase and a digit')
		
		if password_repeat != password:
			errors.append('The two passwords do not match')

		if not errors:
			salt = bcrypt.gensalt()
			user['password'] = bcrypt.hashpw(password.encode('utf-8'), salt)
			db.update_user(user)
			return redirect( url_for('auth.login') )

		for error in errors:
			flash(error, 'danger')

		
	return render_template('auth/resetpw.html')