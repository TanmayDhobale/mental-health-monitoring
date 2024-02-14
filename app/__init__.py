from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Flask-Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)  # Initialize with app
login_manager.login_view = 'login'  # Assuming 'login' is the function name or endpoint for your login view
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)  # Initialize Flask-Migrate

from app import routes
from .models import User  # Make sure your models are correctly imported

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
