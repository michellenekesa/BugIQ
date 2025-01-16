import os

class Config:
    # Basic Flask configuration
    SECRET_KEY = 'dev'  # Change this to a random string in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bug_severity.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model configuration
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'improved_bug_severity_model_v2.joblib')
    VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.joblib')