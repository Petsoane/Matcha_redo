from flask import Flask
from matcha.models import DB
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'

logged_in_users = {}
valid_users = []

db = DB()
# Create the database tables
db.create_tables()


socket = SocketIO(app, Threaded=True, cors_allowed_origin='*')

# import blueprints
from matcha.views.auth import auth
from matcha.views.home import main

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(main)