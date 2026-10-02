import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Ensure stopwords are available
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))

ps = PorterStemmer()

def clean_text(text: str) -> str:
    """
    Cleans raw news text by:
    1. Removing URLs, special characters, digits, and extra spaces
    2. Converting to lowercase
    3. Removing English stopwords
    4. Applying Porter Stemming (reducing words to root form)
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Remove URLs (http/https/www)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    
    # Remove HTML tags if present
    text = re.sub(r'<.*?>', ' ', text)
    
    # Keep only alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Convert to lowercase and split into tokens
    words = text.lower().split()
    
    # Filter stopwords and apply stemming
    cleaned_tokens = [ps.stem(w) for w in words if w not in stop_words and len(w) > 2]
    
    return " ".join(cleaned_tokens)
