import os
import sys
import json
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Project root path setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.train import train
from src.predict import predict_news, MODEL_PATH, VECTORIZER_PATH

METRICS_PATH = os.path.join(PROJECT_ROOT, "models", "metrics.json")

def load_metrics():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

# Custom CSS styling for a modern UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .card-real {
        background-color: #ECFDF5;
        border-left: 6px solid #10B981;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .card-fake {
        background-color: #FEF2F2;
        border-left: 6px solid #EF4444;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #E2E8F0;
        color: #334155;
        margin-right: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/news.png", width=110)
    st.title("About the System")
    st.write(
        "This application uses **Natural Language Processing (NLP)** and **Machine Learning** "
        "to analyze linguistic patterns, emotional markers, and syntax in news articles to predict their authenticity."
    )
    
    st.divider()
    metrics = load_metrics()
    if metrics:
        st.subheader("📊 Active Model Stats")
        st.write(f"**Algorithm:** {metrics.get('model_name', 'N/A')}")
        st.metric("Test Accuracy", f"{metrics.get('accuracy', 0)}%")
        st.metric("F1-Score", f"{metrics.get('f1_score', 0)}%")
        st.caption(f"Trained on: {metrics.get('trained_at', 'N/A')}")
    else:
        st.warning("⚠️ No trained model found yet. Go to the **'Train Model'** tab to train one!")

    st.divider()
    st.subheader("📁 Kaggle Dataset Guide")
    st.caption("To train on the full ~45,000 Kaggle articles:")
    st.markdown("""
    1. Download [ISOT Fake & Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset).
    2. Place `True.csv` and `Fake.csv` into the `data/` folder.
    3. Click **'Retrain Model'** in the app!
    """)

# ----------------- MAIN CONTENT -----------------
st.markdown('<div class="main-title">📰 Fake News Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze text content and determine news credibility using trained Machine Learning models.</div>', unsafe_allow_html=True)

# Tabs
tab_detect, tab_train, tab_performance = st.tabs(["🔍 Detect News", "⚙️ Train / Retrain Dataset", "📈 Model Analytics"])

# ================= TAB 1: DETECT NEWS =================
with tab_detect:
    st.subheader("Test an Article")
    
    # Pre-fill sample buttons
    col_sample1, col_sample2 = st.columns(2)
    sample_text = ""
    with col_sample1:
        if st.button("📰 Load Real News Sample"):
            st.session_state['input_title'] = "NASA James Webb Space Telescope discovers oldest known galaxy"
            st.session_state['input_text'] = (
                "Astronomers using the James Webb Space Telescope have identified a galaxy "
                "that formed just 300 million years after the Big Bang. Peer-reviewed findings "
                "published in Nature confirm spectral measurements consistent with early cosmic expansion."
            )
    with col_sample2:
        if st.button("⚠️ Load Fake News Sample"):
            st.session_state['input_title'] = "Secret miracle root cures all forms of cancer in 48 hours"
            st.session_state['input_text'] = (
                "Doctors are stunned! This ancient mountain herb destroys every cancer cell in two days. "
                "Government scientists are hiding the miracle remedy to protect pharmaceutical trillion-dollar profits. "
                "Order now before it is banned worldwide!"
            )

    title_val = st.session_state.get('input_title', '')
    text_val = st.session_state.get('input_text', '')

    news_title = st.text_input("News Headline / Title (Optional)", value=title_val, placeholder="e.g. Breaking: New scientific breakthrough announced...")
    news_body = st.text_area("News Article Content / Body Text", value=text_val, height=180, placeholder="Paste the news story or paragraph here...")

    if st.button("🚀 Analyze Article", type="primary", use_container_width=True):
        full_content = (news_title + " " + news_body).strip()
        
        if not full_content:
            st.warning("Please enter some text or headline to analyze.")
        elif not os.path.exists(MODEL_PATH):
            st.error("Model is not trained yet! Please open the '⚙️ Train / Retrain Dataset' tab and click Train Model.")
        else:
            with st.spinner("Analyzing text patterns and vocabulary..."):
                try:
                    result = predict_news(full_content)
                    
                    if 'error' in result:
                        st.error(result['error'])
                    else:
                        is_real = result['label'] == 'REAL'
                        
                        col1, col2 = st.columns([1.2, 1])
                        
                        with col1:
                            if is_real:
                                st.markdown(f"""
                                <div class="card-real">
                                    <h2 style="color: #065F46; margin:0;">✅ VERDICT: REAL NEWS</h2>
                                    <p style="color: #047857; margin: 5px 0 0 0; font-size: 1.1rem;">
                                        Confidence Score: <b>{result['confidence']}%</b>
                                    </p>
                                    <p style="color: #374151; font-size: 0.95rem; margin-top: 8px;">
                                        The linguistic patterns, source structure, and vocabulary in this article align closely with verified news reporting.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="card-fake">
                                    <h2 style="color: #991B1B; margin:0;">🚨 VERDICT: FAKE NEWS</h2>
                                    <p style="color: #B91C1C; margin: 5px 0 0 0; font-size: 1.1rem;">
                                        Confidence Score: <b>{result['confidence']}%</b>
                                    </p>
                                    <p style="color: #374151; font-size: 0.95rem; margin-top: 8px;">
                                        Warning: This article exhibits sensationalist syntax, exaggerated phrasing, or unverified claims common in misleading content.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)

                        with col2:
                            st.write("### Probability Meter")
                            st.write(f"**Real:** {result['probability_real']}%")
                            st.progress(result['probability_real'] / 100.0)
                            st.write(f"**Fake:** {result['probability_fake']}%")
                            st.progress(result['probability_fake'] / 100.0)

                        if result.get('key_tokens'):
                            st.write("---")
                            st.write("#### 🔑 Influential Keywords Detected by Model:")
                            tags_html = "".join([f'<span class="badge">{token}</span>' for token in result['key_tokens']])
                            st.markdown(tags_html, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

# ================= TAB 2: TRAIN DATASET =================
with tab_train:
    st.subheader("Model Training & Dataset Pipeline")
    st.write(
        "Train the machine learning model directly on your dataset. "
        "The system will preprocess the text, apply TF-IDF feature extraction, "
        "compare multiple classifiers, and save the best performing model."
    )

    data_info_col1, data_info_col2 = st.columns(2)
    with data_info_col1:
        st.info("💡 **Ready Starter Dataset:** The app comes with a pre-configured starter dataset so you can train and test immediately.")
    with data_info_col2:
        st.success("📁 **Full Kaggle Dataset:** If you drop `True.csv` and `Fake.csv` into `data/`, the training script will automatically train on all 45,000 articles!")

    if st.button("🔥 Start Model Training", type="primary"):
        with st.status("Training in progress...", expanded=True) as status:
            st.write("1️⃣ Checking dataset files...")
            st.write("2️⃣ Preprocessing text (cleaning, stopwords removal, stemming)...")
            st.write("3️⃣ Vectorizing with TF-IDF (10,000 features, 1-2 n-grams)...")
            st.write("4️⃣ Training Passive-Aggressive Classifier & Logistic Regression...")
            
            try:
                metrics_res = train()
                status.update(label="✅ Training Completed Successfully!", state="complete", expanded=False)
                st.success(f"🎉 Model trained with **{metrics_res['accuracy']}% accuracy**!")
                st.rerun()
            except Exception as e:
                status.update(label="❌ Training Failed", state="error")
                st.error(f"Error during training: {str(e)}")

# ================= TAB 3: MODEL ANALYTICS =================
with tab_performance:
    st.subheader("Model Evaluation & Architecture")
    metrics = load_metrics()
    
    if metrics:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Accuracy", f"{metrics.get('accuracy', 0)}%")
        col_m2.metric("Precision", f"{metrics.get('precision', 0)}%")
        col_m3.metric("Recall", f"{metrics.get('recall', 0)}%")
        col_m4.metric("F1-Score", f"{metrics.get('f1_score', 0)}%")

        st.write("---")
        st.write("#### 📊 Confusion Matrix")
        cm = metrics.get('confusion_matrix', [[0, 0], [0, 0]])
        st.write(f"- **True Negatives (Correctly identified Fake):** {cm[0][0]}")
        st.write(f"- **False Positives (Fake wrongly marked Real):** {cm[0][1]}")
        st.write(f"- **False Negatives (Real wrongly marked Fake):** {cm[1][0]}")
        st.write(f"- **True Positives (Correctly identified Real):** {cm[1][1]}")
    else:
        st.info("Train the model first to inspect evaluation metrics and confusion matrix.")

    st.write("---")
    st.write("#### 🧠 NLP & ML Pipeline Details")
    st.markdown("""
    - **Step 1: Text Preprocessing**: Strips non-alphabetic characters, converts to lowercase, filters common stopwords, and stems words using the Porter Stemmer.
    - **Step 2: Feature Extraction**: Uses **TF-IDF (Term Frequency - Inverse Document Frequency)** with unigram & bigram combinations (`ngram_range=(1,2)`).
    - **Step 3: Classification**: Compares **Passive-Aggressive Classifier** (online learning algorithm optimized for text streams) against **Logistic Regression**.
    """)
