from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db, bcrypt
from .forms import RegistrationForm, LoginForm, ProfileForm
from .models import User, DailyLog
from flask_login import login_user, logout_user, login_required, current_user
from .text_analysis import analyze_text, get_sentiment, analyze_emotion  # Ensure these functions are correctly implemented
from .models import DailyLog
from . import db
import spacy
from flask import flash, session
from textblob import TextBlob
from nrclex import NRCLex
from collections import Counter

main = Blueprint('main', __name__)
nlp = spacy.load('en_core_web_sm')

@main.route('/')
def home():
    return render_template('home.html')
def home():
    analysis_results = None
    if 'analysis' in session:
        analysis_results = session['analysis']
    return render_template('home.html', analysis_results=analysis_results)

@main.route('/logout')
@login_required
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
        daily_log_content = request.form.get('daily_log')
        if daily_log_content:
            analysis_results = comprehensive_analysis(daily_log_content)
            if analysis_results:  # Check if analysis_results is not None
                flash(f"Analysis Complete. Sentiment: {analysis_results.get('sentiment', 'N/A')}, Top Emotion: {analysis_results.get('top_emotion', 'N/A')}")
            else:
                flash("Analysis failed. Please try again.")
            return redirect(url_for('main.home'))
        else:
            flash('Please enter some text for analysis.', 'info')
    return render_template('entry_form.html')


@main.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    daily_logs = DailyLog.query.filter_by(user_id=user_id).all()  # Fetch logs for current user
    return render_template('dashboard.html', daily_logs=daily_logs)

def analyze_text(text):
    doc = nlp(text)
    for sentence in doc.sents:
        print(f"Sentence: {sentence.text}")
        for token in sentence:
            print(f"{token.text} - POS: {token.pos_}, Lemma: {token.lemma_}")
        for ent in sentence.ents:
            print(f"Entity: {ent.text}, Type: {ent.label_}")


def comprehensive_analysis(text):
    try:
        # Assuming your analysis might set these values based on the text
        sentiment = get_sentiment(text)
        top_emotion = analyze_emotion(text)
        # Make sure the above functions return sensible defaults if their analysis fails
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error in text analysis: {e}")
        return {'sentiment': 0, 'top_emotion': 'unknown'}  # Return default values in case of an error

    return {
        'sentiment': sentiment,
        'top_emotion': top_emotion,
    }



def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 to 1 where -1 is negative and 1 is positive
    return sentiment

def analyze_emotion(text):
    emotion = NRCLex(text)
    emotion_dict = dict(emotion.affect_frequencies)  # Convert to dict if not already one
    # Consider filtering or processing the emotion dictionary as needed
    return emotion_dict

@main.route('/analyze')
def analyze():
    # Your code here
    return render_template('analyze.html')


def comprehensive_analysis(text):
    try:
        sentiment_score = get_sentiment(text)
        emotion_results = analyze_emotion(text)
        top_emotion = max(emotion_results, key=emotion_results.get)  # Adjusted to get the key with the highest value
        return {
            'sentiment': sentiment_score,
            'top_emotion': top_emotion,
        }
    except Exception as e:
        print(f"Error in text analysis: {e}")
        return {'sentiment': 0, 'top_emotion': 'unknown'}
