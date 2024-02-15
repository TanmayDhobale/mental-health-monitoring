from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db, bcrypt
from .forms import RegistrationForm, LoginForm, ProfileForm
from .models import User, DailyLog
from flask_login import login_user, logout_user, login_required, current_user
from .text_analysis import analyze_text, get_sentiment, analyze_emotion
from .models import DailyLog
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))




@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with this email already exists. Please log in.', 'info')
            return redirect(url_for('main.login'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('profile.html', title='Profile', form=form)

@main.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        daily_log_content = request.form['daily_log']
        if current_user.is_authenticated:
            user_id = current_user.id
            new_entry = DailyLog(content=daily_log_content, user_id=user_id)
            db.session.add(new_entry)
            db.session.commit()
            # Redirect to a page like the user's dashboard after saving the entry
            return redirect(url_for('main.analyze'))  
        else:
            flash('You need to login to submit entries.', 'warning')
            return redirect(url_for('main.login'))
    return render_template('entry_form.html')


@main.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    daily_logs = DailyLog.query.filter_by(user_id=user_id).all()  # Fetch logs for current user
    return render_template('dashboard.html', daily_logs=daily_logs)


@main.route('/analyze', methods=['GET'])
def analyze():
    if request.method == 'POST':
        text = request.form['text']
        analysis_results = comprehensive_analysis(text)
        return render_template('analyze.html', analysis_results=analysis_results)

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def analyze_emotion(text):
    emotion = NRCLex(text)
    return emotion.top_emotions

def comprehensive_analysis(text):
    sentiment = get_sentiment(text)
    emotions = analyze_emotion(text)
    sentiment_text = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    return {"sentiment": sentiment_text, "emotions": emotions}

if __name__ == '__main__':
    main.run(debug=True)