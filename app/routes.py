from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user , login_required
from .models import User 





main = Blueprint('main', __name__)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Assume we get 'username' and 'email' from a form
        username = request.form.get('username')
        email = request.form.get('email')
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@main.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')