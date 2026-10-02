import os
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(DATA_DIR, "news_dataset.csv")

SAMPLE_ARTICLES = [
    # Real News (Label = 1)
    {"title": "NASA James Webb Space Telescope discovers oldest known galaxy",
     "text": "Astronomers using the James Webb Space Telescope have identified a galaxy that formed just 300 million years after the Big Bang. Peer-reviewed findings published in Nature confirm spectral measurements consistent with early cosmic expansion.",
     "label": 1},
    {"title": "Federal Reserve holds interest rates steady amid slowing inflation",
     "text": "The central bank decided to maintain its benchmark interest rate target range following the Federal Open Market Committee meeting. Chair Jerome Powell stated that economic indicators show moderate growth and steady labor markets.",
     "label": 1},
    {"title": "World Health Organization updates guidance on seasonal influenza vaccination",
     "text": "The WHO released updated recommendations for annual flu vaccines, emphasizing immunization for healthcare workers, elderly adults, and immunocompromised individuals ahead of the winter season.",
     "label": 1},
    {"title": "European Union passes landmark legislation to regulate artificial intelligence",
     "text": "Lawmakers in the European Parliament voted to approve the AI Act, establishing comprehensive risk-based guidelines for machine learning systems used across healthcare, law enforcement, and critical infrastructure.",
     "label": 1},
    {"title": "Global renewable energy capacity surges to record high in recent quarter",
     "text": "The International Energy Agency reported an unprecedented increase in solar and wind power installations worldwide, driven by declining hardware costs and national clean energy incentives.",
     "label": 1},
    {"title": "Researchers develop promising new antibiotic targeting resistant bacteria",
     "text": "A team of microbiologists at Harvard University and MIT synthesized a novel compound capable of overcoming multi-drug resistant superbugs in preclinical laboratory trials.",
     "label": 1},
    {"title": "United Nations climate summit concludes with historic decarbonization agreement",
     "text": "Delegates from over 190 countries finalized an agreement committing to triple renewable energy capacity and accelerate transitions away from fossil fuels by 2030.",
     "label": 1},
    {"title": "Electric vehicle battery breakthrough achieves 600 mile range in tests",
     "text": "Engineers published verified laboratory data demonstrating a solid-state lithium battery prototype capable of over 1000 fast-charge cycles with minimal degradation.",
     "label": 1},
    {"title": "Stock markets close higher as tech earnings beat analyst forecasts",
     "text": "Major indices gained ground today following positive quarterly financial reports from leading semiconductor and cloud computing corporations.",
     "label": 1},
    {"title": "Global shipping routes adjust after navigational updates in the Red Sea",
     "text": "Maritime authorities and international transport alliances have issued updated route advisories to ensure safe commercial navigation across international waters.",
     "label": 1},
    {"title": "Public transit agency announces major subway system modernization project",
     "text": "City officials unveiled a multi-billion dollar infrastructure initiative to replace aging signals, improve accessibility, and upgrade rolling stock over the next decade.",
     "label": 1},
    {"title": "Archaeologists uncover ancient trading post along historical Silk Road",
     "text": "Excavations in Central Asia revealed coins, pottery, and commercial records dating back to the 5th century, shedding new light on historical trade connections.",
     "label": 1},

    # Fake News (Label = 0)
    {"title": "Secret miracle root cures all forms of cancer in 48 hours big pharma does not want you to know",
     "text": "Doctors are stunned! This ancient mountain herb destroys every cancer cell in two days. Government scientists are hiding the miracle remedy to protect pharmaceutical trillion-dollar profits. Order now before it is banned!",
     "label": 0},
    {"title": "Aliens landed in secret desert base and signed treaty with world leaders shocking leaked tape",
     "text": "Top secret whistleblower leaks 100% genuine footage of extraterrestrial beings meeting underground politicians. The global shadow government will announce mandatory chip implants next week according to anonymous insider.",
     "label": 0},
    {"title": "Drink boiled lemon water and salt to permanently reverse aging and eliminate all viruses",
     "text": "Renowned guru reveals that simply drinking boiling saltwater each morning activates hidden DNA receptors that make your biological age drop by 30 years instantly. Hospitals refuse to verify this simple home trick!",
     "label": 0},
    {"title": "Government quietly installs mind control towers disguised as 5G mobile antennas nationwide",
     "text": "Uncovered secret blueprint shows that cellular telecommunication towers are emitting invisible neurological frequencies designed to manipulate voting patterns and enforce compliance. Share this before it gets deleted!",
     "label": 0},
    {"title": "Celebrity billionaire admits fake moon landing filmed in Hollywood studio on live broadcast",
     "text": "During an unscripted commercial break interview, the famous tech CEO accidentally revealed classified documents proving that space exploration is a staged theatrical performance designed to extract taxpayer funds.",
     "label": 0},
    {"title": "Microwave ovens create radioactive toxic molecules that turn water poisonous instantly",
     "text": "Terrifying study discovered by independent blogger shows that warming your food for even ten seconds mutates genetic structures and creates lethal radiation poisoning in standard kitchen meals. Throw your microwave away immediately!",
     "label": 0},
    {"title": "Secret banking cartel declares cash illegal starting next Monday worldwide",
     "text": "Shocking leaks from unverified forum posts confirm that all physical currency bills will be confiscated by midnight and replaced with biometric tracking tokens. Banks will seize all private savings without notice!",
     "label": 0},
    {"title": "Miracle magnetic bracelet pulls all toxins and disease directly out through your wrists",
     "text": "Clinical experiments suppressed by elite doctors demonstrate that wearing this quantum ion magnetic band purges every illness, diabetes, and heart problem within 24 hours without diet or medicine!",
     "label": 0},
    {"title": "Ancient prophecy predicted meteorite containing pure gold will hit city center tomorrow",
     "text": "Mystic prophecies circulating on social media claim a golden asteroid sent by ancient civilizations is hurtling towards earth and will make all residents instant billionaires if they gather at the monument.",
     "label": 0},
    {"title": "Scientists caught admitting global weather is controlled by secret cloud generator machine",
     "text": "Leaked underground audio reveals high-ranking bureaucrats laughing about manually pressing buttons to create rainstorms and snow to manipulate agricultural commodity prices. Mainstream media silent!",
     "label": 0},
    {"title": "Famous Hollywood actor faked death and is living on secret private island with historical figures",
     "text": "Shocking photographs taken with a zoom lens allegedly prove that deceased celebrities are all alive and well, partying at an undisclosed billionaire resort in the Bermuda Triangle.",
     "label": 0},
    {"title": "Eating raw onion peelings under your pillow attracts wealth and cures insomnia overnight",
     "text": "Ancient superstition proven true by underground researchers! Placing pungent root vegetables beneath your bedding realigns your aura and attracts unexpected lottery windfalls within seven days guaranteed.",
     "label": 0}
]

def load_or_create_dataset():
    """
    Loads dataset:
    1. If True.csv and Fake.csv exist in data/ (Kaggle ISOT format), merges and cleans them.
    2. Otherwise, creates and loads a starter dataset with balanced real and fake news articles.
    """
    true_csv = os.path.join(DATA_DIR, "True.csv")
    fake_csv = os.path.join(DATA_DIR, "Fake.csv")

    if os.path.exists(true_csv) and os.path.exists(fake_csv):
        print("Found Kaggle ISOT dataset (True.csv & Fake.csv)! Loading full dataset...")
        df_true = pd.read_csv(true_csv, on_bad_lines='skip')
        df_fake = pd.read_csv(fake_csv, on_bad_lines='skip')
        
        # Helper to extract content column
        def get_text_content(d):
            cols = [c.lower() for c in d.columns]
            title_col = d.columns[cols.index('title')] if 'title' in cols else None
            text_col = d.columns[cols.index('text')] if 'text' in cols else None
            
            if title_col and text_col:
                return d[title_col].fillna('').astype(str) + " " + d[text_col].fillna('').astype(str)
            elif text_col:
                return d[text_col].fillna('').astype(str)
            elif title_col:
                return d[title_col].fillna('').astype(str)
            else:
                return d.iloc[:, 0].fillna('').astype(str)

        df_true['content'] = get_text_content(df_true)
        df_true['label'] = 1
        
        df_fake['content'] = get_text_content(df_fake)
        df_fake['label'] = 0
        
        df = pd.concat([df_true[['content', 'label']], df_fake[['content', 'label']]], ignore_index=True)
        df = df[df['content'].str.strip() != '']
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        print(f"Loaded {len(df)} total articles from Kaggle files.")
        return df

    # If already created starter dataset exists, load it
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        return df

    # Otherwise, generate starter dataset
    print("Creating initial starter dataset with sample Real and Fake news...")
    df = pd.DataFrame(SAMPLE_ARTICLES)
    df['content'] = df['title'] + " " + df['text']
    df = df[['content', 'label']]
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Created {DATASET_PATH} with {len(df)} articles.")
    return df

if __name__ == "__main__":
    df = load_or_create_dataset()
    print(f"Dataset ready with shape: {df.shape}")
    print(f"Class distribution:\n{df['label'].value_counts()}")
