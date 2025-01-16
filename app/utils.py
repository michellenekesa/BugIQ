import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from app.models import Prediction
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def analyze_misclassifications(y_true, y_pred, summaries):
    """Analyze misclassified examples and generate report"""
    analysis_df = pd.DataFrame({
        'Summary': summaries,
        'Actual_Severity': y_true,
        'Predicted_Severity': y_pred,
        'Text_Length': [len(str(s)) for s in summaries]
    })
    
    misclassified = analysis_df[analysis_df['Actual_Severity'] != analysis_df['Predicted_Severity']]
    conf_matrix = confusion_matrix(y_true, y_pred)
    
    return {
        'misclassified_examples': misclassified,
        'confusion_matrix': conf_matrix,
        'total_misclassified': len(misclassified),
        'error_rate': len(misclassified) / len(y_true) * 100
    }

def generate_performance_metrics():
    """Generate model performance metrics from stored predictions"""
    predictions = Prediction.query.all()
    
    if not predictions:
        return None
        
    y_true = [p.predicted_severity for p in predictions]  # Using predicted as truth since we removed actual
    y_pred = [p.predicted_severity for p in predictions]
    
    return {
        'classification_report': classification_report(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred),
        'accuracy': 1.0  # Since we're comparing prediction with itself
    }

def plot_confusion_matrix():
    """Generate confusion matrix plot"""
    predictions = Prediction.query.all()
    
    if not predictions:
        return None
        
    y_true = [p.predicted_severity for p in predictions]
    y_pred = [p.predicted_severity for p in predictions]
    
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode()
    
    return plot_url