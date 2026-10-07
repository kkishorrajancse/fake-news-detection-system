import os
import sys
import json
from flask import Flask, render_template, request, jsonify

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.train import train
from src.predict import predict_news, MODEL_PATH

app = Flask(__name__)

METRICS_PATH = os.path.join(PROJECT_ROOT, "models", "metrics.json")

def get_metrics():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

@app.route('/')
def home():
    metrics = get_metrics()
    model_ready = os.path.exists(MODEL_PATH)
    return render_template('index.html', metrics=metrics, model_ready=model_ready)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    title = data.get('title', '').strip()
    text = data.get('text', '').strip()
    
    full_content = (title + " " + text).strip()
    if not full_content:
        return jsonify({'error': 'Please enter news headline or article content to analyze.'}), 400
    
    if not os.path.exists(MODEL_PATH):
        return jsonify({'error': 'Model has not been trained yet. Please click "Train Model" first!'}), 400
    
    try:
        result = predict_news(full_content)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def trigger_training():
    try:
        metrics = train()
        return jsonify({'success': True, 'metrics': metrics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def fetch_metrics():
    metrics = get_metrics()
    return jsonify(metrics or {})

import webbrowser
import threading

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Fake News Detection Website on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)


