# 📰 Fake News Detection System

A Machine Learning and Natural Language Processing (NLP) web application that classifies news articles as **Real** or **Fake** by analyzing linguistic structures, patterns, and vocabulary.

---

## 🌟 Key Features
- **Interactive Web Interface**: Built with [Streamlit](https://streamlit.io/) for instant predictions.
- **In-App & CLI Model Training**: Train or retrain models directly through the web UI or from the command line.
- **NLP Text Preprocessor**: Cleans raw text, strips noise, removes stopwords, and applies Porter Stemming.
- **TF-IDF Feature Extraction**: Evaluates unigrams and bigrams (`ngram_range=(1,2)`) across 10,000 vocabulary features.
- **High-Accuracy ML Classifiers**: Evaluates **Passive-Aggressive Classifier** and **Logistic Regression**, saving the top model.
- **Explainability & Transparency**: Displays confidence percentages and highlights top keywords driving the prediction.
- **Full Kaggle Dataset Ready**: Built-in support for the 45,000-article Kaggle ISOT dataset (`True.csv` and `Fake.csv`).

---

## 📂 Project Structure

```text
ML PROJECT ANTIGRAVITY/
│
├── data/
│   ├── setup_data.py          # Dataset loader & starter dataset generator
│   ├── news_dataset.csv       # Pre-configured starter dataset (auto-generated)
│   ├── True.csv               # (Optional) Kaggle Real News articles
│   └── Fake.csv               # (Optional) Kaggle Fake News articles
│
├── models/
│   ├── fake_news_model.pkl    # Serialized trained machine learning model
│   ├── tfidf_vectorizer.pkl   # Serialized TF-IDF vectorizer
│   └── metrics.json           # Accuracy, precision, recall, and confusion matrix
│
├── src/
│   ├── preprocess.py          # NLP cleaning, tokenization, and stemming
│   ├── train.py               # Model training, evaluation, and export pipeline
│   └── predict.py             # Real-time inference engine
│
├── templates/
│   └── index.html             # HTML5 Responsive Web Interface
├── static/
│   ├── css/style.css          # Custom styling
│   └── js/app.js              # Dynamic AJAX frontend logic
├── flask_app.py               # Flask Web Server (Custom HTML/CSS Website)
├── app.py                     # Streamlit Web Application (Data Science Dashboard)
├── requirements.txt           # Python library dependencies
└── README.md                  # Project documentation & guide
```

---

## 🚀 Quick Start Guide

### Step 1: Open Terminal in Project Folder
Open your Command Prompt / PowerShell:
```powershell
cd "c:\Users\kisho\OneDrive\Documents\ML PROJECT ANTIGRAVITY"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Train the Model
```powershell
python src/train.py
```

### Step 4: Run the Web App (Choose Your Favorite!)

* **Option A: Full Modern Website (HTML, CSS, JS + Flask)**:
  ```powershell
  python flask_app.py
  ```
  Open browser at: **`http://127.0.0.1:5000`**

* **Option B: Streamlit Data Science Dashboard**:
  ```powershell
  streamlit run app.py
  ```
  Open browser at: **`http://localhost:8501`**

---

## 📊 Using the Full Kaggle ISOT Dataset (Optional)
To train the model on the full benchmark dataset of ~45,000 news articles:
1. Go to [Kaggle Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset).
2. Download and unzip the archive.
3. Place `True.csv` and `Fake.csv` inside the `data/` folder.
4. Run `python src/train.py` or click **"Start Model Training"** in the Streamlit app.
