import os
import sys
import json
import joblib
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocess import clean_text
from data.setup_data import load_or_create_dataset

def train():
    print("=" * 60)
    print("🚀 FAKE NEWS DETECTION SYSTEM: MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # 1. Load Dataset
    print("\n[Step 1/5] Loading dataset...")
    df = load_or_create_dataset()
    print(f"Loaded {len(df)} records. Real: {(df['label'] == 1).sum()} | Fake: {(df['label'] == 0).sum()}")

    # 2. Text Preprocessing
    print("\n[Step 2/5] Cleaning and preprocessing text (NLP)...")
    df['cleaned'] = df['content'].apply(clean_text)
    
    # Remove any empty cleaned text
    df = df[df['cleaned'].str.strip() != '']
    X = df['cleaned']
    y = df['label']

    # 3. Train/Test Split
    test_ratio = 0.2 if len(df) > 50 else 0.25
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_ratio, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} samples | Testing set: {len(X_test)} samples")

    # 4. Feature Extraction: TF-IDF
    print("\n[Step 3/5] Vectorizing text with TF-IDF (n-grams: 1-2)...")
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # 5. Model Training & Comparison
    print("\n[Step 4/5] Training Machine Learning Models...")
    
    # Passive-Aggressive Classifier
    pa_model = PassiveAggressiveClassifier(max_iter=100, random_state=42)
    pa_model.fit(X_train_tfidf, y_train)
    pa_preds = pa_model.predict(X_test_tfidf)
    pa_acc = accuracy_score(y_test, pa_preds)

    # Logistic Regression
    lr_model = LogisticRegression(max_iter=200, random_state=42)
    lr_model.fit(X_train_tfidf, y_train)
    lr_preds = lr_model.predict(X_test_tfidf)
    lr_acc = accuracy_score(y_test, lr_preds)

    print(f"   • Passive-Aggressive Classifier Accuracy: {pa_acc * 100:.2f}%")
    print(f"   • Logistic Regression Accuracy:           {lr_acc * 100:.2f}%")

    # Select best model
    if pa_acc >= lr_acc:
        best_model = pa_model
        best_name = "Passive-Aggressive Classifier"
        best_preds = pa_preds
        best_acc = pa_acc
    else:
        best_model = lr_model
        best_name = "Logistic Regression"
        best_preds = lr_preds
        best_acc = lr_acc

    # Metrics
    prec = precision_score(y_test, best_preds, zero_division=0)
    rec = recall_score(y_test, best_preds, zero_division=0)
    f1 = f1_score(y_test, best_preds, zero_division=0)
    cm = confusion_matrix(y_test, best_preds).tolist()

    print("\n" + "-" * 60)
    print(f"🏆 Best Model: {best_name}")
    print(f"   Accuracy:  {best_acc * 100:.2f}%")
    print(f"   Precision: {prec * 100:.2f}%")
    print(f"   Recall:    {rec * 100:.2f}%")
    print(f"   F1-Score:  {f1 * 100:.2f}%")
    print(f"   Confusion Matrix: {cm}")
    print("-" * 60)

    # 6. Save Artifacts
    print("\n[Step 5/5] Saving model and vectorizer...")
    models_dir = os.path.join(PROJECT_ROOT, "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "fake_news_model.pkl")
    vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    metrics_path = os.path.join(models_dir, "metrics.json")

    joblib.dump(best_model, model_path)
    joblib.dump(tfidf, vectorizer_path)

    metrics_data = {
        "model_name": best_name,
        "accuracy": round(best_acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "total_samples": len(df),
        "confusion_matrix": cm,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=4)

    print(f" Saved Model:      {model_path}")
    print(f" Saved Vectorizer: {vectorizer_path}")
    print(f" Saved Metrics:    {metrics_path}")
    print("\n Training successfully completed!")
    return metrics_data

if __name__ == "__main__":
    train()
