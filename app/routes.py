from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Prediction
from app import db
import joblib
import os
import logging
import re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Set NLTK data path to desktop location
nltk.data.path.append('/Users/michellenekesa/Desktop/nltk_data')

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

def load_model():
    """Load model and vectorizer within application context"""
    try:
        model_path = current_app.config['MODEL_PATH']
        vectorizer_path = current_app.config['VECTORIZER_PATH']
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            return None, None
            
        if not os.path.exists(vectorizer_path):
            logger.error(f"Vectorizer file not found at {vectorizer_path}")
            return None, None
            
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        logger.info("Model and vectorizer loaded successfully")
        return model, vectorizer
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None

def preprocess_text(text):
    """Preprocess the input text"""
    try:
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]
        return ' '.join(tokens)
    except Exception as e:
        logger.error(f"Text preprocessing error: {str(e)}")
        return ''

@main.route('/')
@login_required
def dashboard():
    try:
        predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.id.desc()).all()
        return render_template('dashboard.html', predictions=predictions)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        flash('Error loading dashboard', 'error')
        return render_template('dashboard.html', predictions=[])

@main.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        model, vectorizer = load_model()
        if model is None or vectorizer is None:
            return jsonify({'error': 'Model not loaded. Please check model files.'}), 500

        summary = request.form.get('summary', '').strip()
        component = request.form.get('component', '').strip()

        if not summary or not component:
            return jsonify({'error': 'Summary and component are required'}), 400

        # Preprocess text
        processed_text = preprocess_text(f"{summary} {component}")
        if not processed_text:
            return jsonify({'error': 'Error processing text'}), 500

        # Transform text
        features = vectorizer.transform([processed_text])
        
        # Make prediction
        severity = model.predict(features)[0]

        # Save prediction
        prediction = Prediction(
            user_id=current_user.id,
            summary=summary,
            component=component,
            predicted_severity=severity
        )
        db.session.add(prediction)
        db.session.commit()

        return jsonify({'severity': severity})
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Error making prediction'}), 500

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))