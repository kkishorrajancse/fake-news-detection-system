import os
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TRUE_CSV = os.path.join(DATA_DIR, "True.csv")
FAKE_CSV = os.path.join(DATA_DIR, "Fake.csv")

REAL_INDIAN_NEWS = [
    {"title": "M. K. Stalin serves as Chief Minister of Tamil Nadu",
     "text": "M. K. Stalin is the official Chief Minister of Tamil Nadu leading the DMK government from Chennai following state assembly elections.",
     "label": 1, "label_norm": "REAL"},
    {"title": "Actor Joseph Vijay launches political party TVK in Tamil Nadu",
     "text": "Tamil actor Joseph Vijay officially launched his political party Tamilaga Vettri Kazhagam TVK to contest upcoming elections in Tamil Nadu.",
     "label": 1, "label_norm": "REAL"},
    {"title": "ISRO launches PSLV satellite mission from Sriharikota spaceport",
     "text": "The Indian Space Research Organisation successfully deployed satellites into polar orbit from the Satish Dhawan Space Centre.",
     "label": 1, "label_norm": "REAL"},
    {"title": "Reserve Bank of India maintains benchmark repo interest rate",
     "text": "The Reserve Bank of India Monetary Policy Committee announced key policy interest rates after evaluating economic growth and inflation metrics.",
     "label": 1, "label_norm": "REAL"}
]

FAKE_INDIAN_NEWS = [
    {"title": "Joseph Vijay sworn in as Chief Minister of Tamil Nadu overnight",
     "text": "Viral claims alleging actor Joseph Vijay is the Chief Minister of Tamil Nadu are false. M.K. Stalin is the current Chief Minister.",
     "label": 0, "label_norm": "FAKE"},
    {"title": "Tamil Nadu CM is Joseph Vijay claims viral social media post",
     "text": "Social media posts claiming Joseph Vijay holds the office of Chief Minister in Tamil Nadu are fabricated and debunked by fact checkers.",
     "label": 0, "label_norm": "FAKE"},
    {"title": "Drinking boiled garlic water cures all fever in two hours doctors stunned",
     "text": "Medical experts debunked viral home remedy claims promising immediate cure for all viruses without medicine.",
     "label": 0, "label_norm": "FAKE"}
]

def add_and_retrain():
    print("Adding Indian political and regional news data...")
    if os.path.exists(TRUE_CSV) and os.path.exists(FAKE_CSV):
        df_true = pd.read_csv(TRUE_CSV, on_bad_lines='skip')
        df_fake = pd.read_csv(FAKE_CSV, on_bad_lines='skip')
        
        df_new_true = pd.DataFrame(REAL_INDIAN_NEWS)
        df_new_fake = pd.DataFrame(FAKE_INDIAN_NEWS)
        
        df_true_updated = pd.concat([df_true, df_new_true], ignore_index=True)
        df_fake_updated = pd.concat([df_fake, df_new_fake], ignore_index=True)
        
        df_true_updated.to_csv(TRUE_CSV, index=False)
        df_fake_updated.to_csv(FAKE_CSV, index=False)
        print(f"Added new regional facts! Updated True.csv: {len(df_true_updated)} | Fake.csv: {len(df_fake_updated)}")

if __name__ == "__main__":
    add_and_retrain()
