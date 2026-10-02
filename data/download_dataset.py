import os
import io
import zipfile
import urllib.request
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TRUE_CSV = os.path.join(DATA_DIR, "True.csv")
FAKE_CSV = os.path.join(DATA_DIR, "Fake.csv")

# Reliable direct GitHub zip repository of verified real and fake news articles (George McIntire dataset)
ZIP_URL = "https://raw.githubusercontent.com/joolsa/fake_real_news_dataset/master/fake_or_real_news.csv.zip"

def download_and_setup_dataset():
    print("=" * 60)
    print("📥 AUTOMATED DATASET DOWNLOADER FOR FAKE NEWS DETECTION")
    print("=" * 60)

    print("\n[1/3] Downloading verified news dataset (~11 MB)...")
    print("Please wait 10-20 seconds...")

    try:
        # Download ZIP file into memory
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(ZIP_URL, headers=headers)
        with urllib.request.urlopen(req) as resp:
            zip_data = resp.read()

        print("[2/3] Extracting news articles...")
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            csv_filename = [f for f in z.namelist() if f.endswith('.csv')][0]
            with z.open(csv_filename) as f:
                df = pd.read_csv(f, on_bad_lines='skip')

        print(f"Loaded {len(df)} total articles.")
        print("[3/3] Splitting into True.csv and Fake.csv...")

        # Normalize label column: can be 'REAL'/'FAKE' or 1/0
        if 'label' in df.columns:
            df['label_norm'] = df['label'].astype(str).str.strip().str.upper()
            df_true = df[df['label_norm'].isin(['REAL', '1', 'TRUE'])].copy()
            df_fake = df[df['label_norm'].isin(['FAKE', '0', 'FALSE'])].copy()
        else:
            # Half and half split if unlabeled
            mid = len(df) // 2
            df_true = df.iloc[:mid].copy()
            df_fake = df.iloc[mid:].copy()

        # Save to disk
        df_true.to_csv(TRUE_CSV, index=False)
        df_fake.to_csv(FAKE_CSV, index=False)

        print("\n" + "=" * 60)
        print("🎉 SUCCESS! DATASET FILES CREATED SUCCESSFULLY:")
        print(f"   ✅ {TRUE_CSV} ({len(df_true)} Real News articles)")
        print(f"   ✅ {FAKE_CSV} ({len(df_fake)} Fake News articles)")
        print("=" * 60)
        print("\nNow run: python src/train.py to train your model!")

    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        print("Generating local high-volume dataset backup...")
        # Fallback: Expand news_dataset.csv
        from setup_data import load_or_create_dataset
        df = load_or_create_dataset()
        df[df['label'] == 1].to_csv(TRUE_CSV, index=False)
        df[df['label'] == 0].to_csv(FAKE_CSV, index=False)
        print("✅ Created True.csv and Fake.csv from starter dataset!")

if __name__ == "__main__":
    download_and_setup_dataset()
