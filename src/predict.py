import os
import sys
import numpy as np
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocess import clean_text

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "fake_news_model.pkl")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "models", "tfidf_vectorizer.pkl")

_model = None
_vectorizer = None
_last_mtime = 0

def load_artifacts():
    global _model, _vectorizer, _last_mtime
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            "Model files not found! Please run training first via 'python src/train.py'."
        )
    
    current_mtime = os.path.getmtime(MODEL_PATH)
    if _model is None or _vectorizer is None or current_mtime > _last_mtime:
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
        _last_mtime = current_mtime
    return _model, _vectorizer

def predict_news(text: str):
    """
    Analyzes input text and predicts whether it is REAL or FAKE.
    Returns:
        dict: {
            'label': 'REAL' or 'FAKE',
            'confidence': float (0.0 to 100.0),
            'probability_real': float (0.0 to 1.0),
            'probability_fake': float (0.0 to 1.0),
            'key_tokens': list of top contributing word stems
        }
    """
    model, vectorizer = load_artifacts()
    
    cleaned = clean_text(text)
    if not cleaned:
        return {
            'label': 'UNKNOWN',
            'confidence': 0.0,
            'probability_real': 0.5,
            'probability_fake': 0.5,
            'key_tokens': [],
            'error': 'Text is too short or contains no valid alphabetical words.'
        }
    
    # Vectorize
    vec = vectorizer.transform([cleaned])
    
    # Check if any words matched vocabulary
    if vec.nnz == 0:
        return {
            'label': 'UNKNOWN',
            'confidence': 50.0,
            'probability_real': 50.0,
            'probability_fake': 50.0,
            'key_tokens': [],
            'error': 'Words in this short phrase are not in the dataset vocabulary. Please paste full news headlines or article paragraphs for accurate prediction.'
        }
    
    # Calculate confidence / probability
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(vec)[0]
        prob_fake = float(probs[0])
        prob_real = float(probs[1])
    else:
        # For PassiveAggressiveClassifier, calibrate decision_function with sigmoid
        decision = float(model.decision_function(vec)[0])
        prob_real = 1.0 / (1.0 + np.exp(-decision))
        prob_fake = 1.0 - prob_real

    # Prediction
    is_real = prob_real >= 0.5
    label = "REAL" if is_real else "FAKE"
    confidence = (prob_real if is_real else prob_fake) * 100.0

    # Extract top keywords matching model vocabulary
    feature_names = vectorizer.get_feature_names_out()
    non_zero_indices = vec.nonzero()[1]
    
    # Score features based on TF-IDF weight * model coefficient
    key_tokens = []
    if hasattr(model, 'coef_'):
        coefs = model.coef_[0]
        scored_tokens = []
        for idx in non_zero_indices:
            word = feature_names[idx]
            weight = vec[0, idx] * coefs[idx]
            scored_tokens.append((word, weight))
        
        # If Real, sort descending; if Fake, sort ascending
        if is_real:
            scored_tokens.sort(key=lambda x: x[1], reverse=True)
        else:
            scored_tokens.sort(key=lambda x: x[1])
        key_tokens = [t[0] for t in scored_tokens[:6]]

    return {
        'label': label,
        'confidence': round(confidence, 1),
        'probability_real': round(prob_real * 100, 1),
        'probability_fake': round(prob_fake * 100, 1),
        'key_tokens': key_tokens,
        'cleaned_preview': cleaned[:120] + "..." if len(cleaned) > 120 else cleaned
    }

if __name__ == "__main__":
    test_real = "NASA telescope observes ancient stars confirming standard astrophysical cosmological models."
    test_fake = "Secret miracle tea eliminates all terminal illness in 24 hours doctors furious!"
    
    print("Test Real:", predict_news(test_real))
    print("Test Fake:", predict_news(test_fake))
