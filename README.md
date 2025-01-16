# BugIQ
# Automated Software Bug Severity Prediction

This project leverages machine learning techniques to predict the severity of software bugs, aiming to enhance quality assurance in software development. The solution utilizes Random Forests, Latent Dirichlet Allocation (LDA), and VADER sentiment analysis, with a Flask-based web interface for real-time predictions.

## Features
- Automated bug severity prediction: Classifies bugs into `Critical`, `Major`, `Medium`, or `Trivial`.
- Real-time predictions via an intuitive web-based interface.
- Secure user authentication and prediction history tracking.
- Handles both structured (bug attributes) and unstructured data (bug descriptions).

## Dataset
- **Source**: Eclipse Bug Dataset (558,000+ records from 2002-2022).
- **Preprocessing**:
  - Tokenization, stop-word removal, and stemming.
  - Sentiment analysis using VADER.
  - Topic modeling using LDA.
  - SMOTE for handling class imbalances.
- **Key fields used**: Bug ID, Date Created, Status, Resolution, Priority, Severity, and Summary.

## Technologies
- **Programming Language**: Python
- **Frameworks**: Flask, Jupyter Notebook
- **Machine Learning Algorithm**: Random Forests
- **Database**: SQLite
- **Frontend**: Bootstrap
- **NLP Tools**: VADER, LDA, TF-IDF

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bug-severity-prediction.git
   cd bug-severity-prediction
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the SQLite database:
   ```bash
   python setup_database.py
   ```
5. Run the application:
   ```bash
   flask run
   ```

## Usage
1. Navigate to the Flask application's URL (default: `http://127.0.0.1:5000`).
2. Log in or register as a new user.
3. Submit bug descriptions and affected components via the dashboard.
4. View the predicted severity levels and track past predictions.

## Project Workflow
1. Data preprocessing with TF-IDF, VADER, and LDA.
2. Model training using Random Forests with hyperparameter tuning via RandomizedSearchCV.
3. Deployment using a RESTful Flask API.

## Testing
- Black-box testing ensured functionality and reliability.
- Evaluation metrics:
  - **Precision, Recall, F1-Score, and Accuracy**.
  - Confusion matrix visualized as a heatmap.

## Future Work
- Expand dataset for improved accuracy and generalization.
- Incorporate advanced NLP techniques and feedback loops for continuous learning.
- Integrate with existing bug tracking systems like JIRA or GitHub Issues.

---



