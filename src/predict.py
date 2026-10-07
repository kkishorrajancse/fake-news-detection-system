import os
import sys
import numpy as np
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocess import clean_text
from src.fact_verifier import verify_claim_and_evidence

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
    Multi-source evidence-based prediction gateway.
    Combines ML classification with Named Entity Recognition, Temporal Verification,
    Claim Extraction, and Multi-Source Evidence Retrieval.
    """
    ml_result = {}
    try:
        model, vectorizer = load_artifacts()
        cleaned = clean_text(text)
        if cleaned:
            vec = vectorizer.transform([cleaned])
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(vec)[0]
                prob_fake = float(probs[0])
                prob_real = float(probs[1])
            else:
                decision = float(model.decision_function(vec)[0])
                prob_real = 1.0 / (1.0 + np.exp(-decision))
                prob_fake = 1.0 - prob_real

            is_real = prob_real >= 0.5
            ml_result = {
                'label': "REAL" if is_real else "FAKE",
                'confidence': (prob_real if is_real else prob_fake) * 100.0,
                'probability_real': prob_real * 100,
                'probability_fake': prob_fake * 100
            }
    except Exception:
        pass

    # Fact verification pipeline
    verification = verify_claim_and_evidence(text, ml_result)
    
    # Structure full response maintaining backward compatibility
    prob_real = verification['confidence'] if verification['verdict'] == 'TRUE' else (100.0 - verification['confidence'])
    prob_fake = verification['confidence'] if verification['verdict'] == 'FALSE' else (100.0 - verification['confidence'])
    
    response = {
        'label': verification['verdict'],
        'verdict': verification['verdict'],
        'confidence': verification['confidence'],
        'probability_real': round(max(0.0, min(100.0, prob_real)), 1),
        'probability_fake': round(max(0.0, min(100.0, prob_fake)), 1),
        'claim': verification['claim'],
        'explanation': verification['explanation'],
        'evidence': verification['evidence'],
        'source_credibility': verification['source_credibility'],
        'verification_time': verification['verification_time'],
        'entities': verification['entities']
    }

    return response

if __name__ == "__main__":
    print(predict_news("Joseph Vijay is the Chief Minister of Tamil Nadu."))
