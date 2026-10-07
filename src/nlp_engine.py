import re

# Domain entity & position keywords
POSITIONS = {
    "chief minister": "Chief Minister",
    "cm": "Chief Minister",
    "prime minister": "Prime Minister",
    "pm": "Prime Minister",
    "president": "President",
    "governor": "Governor",
    "minister": "Minister",
    "mayor": "Mayor"
}

LOCATIONS = {
    "tamil nadu": "Tamil Nadu",
    "tamilnadu": "Tamil Nadu",
    "tn": "Tamil Nadu",
    "india": "India",
    "chennai": "Chennai",
    "delhi": "Delhi",
    "mumbai": "Mumbai",
    "kerala": "Kerala",
    "karnataka": "Karnataka"
}

PEOPLE = {
    "joseph vijay": "Joseph Vijay",
    "vijay": "Joseph Vijay",
    "thalapathy vijay": "Joseph Vijay",
    "m. k. stalin": "M. K. Stalin",
    "mk stalin": "M. K. Stalin",
    "stalin": "M. K. Stalin",
    "edappadi palaniswami": "Edappadi K. Palaniswami",
    "eps": "Edappadi K. Palaniswami",
    "jayalalithaa": "J. Jayalalithaa",
    "narendra modi": "Narendra Modi",
    "modi": "Narendra Modi"
}

QUESTION_STARTERS = ["who", "what", "where", "when", "why", "how", "is", "are", "can", "yaar", "ethu", "enge", "eppadi"]
OPINION_MARKERS = ["i think", "i believe", "in my opinion", "seems terrible", "looks bad", "best movie", "worst policy", "my view", "enaku thonudhu"]

def detect_input_type(text: str) -> str:
    """
    Returns one of: 'QUESTION', 'OPINION', 'FACTUAL_CLAIM'
    """
    text_lower = text.strip().lower()
    
    # Check if ends with '?' or starts with question words
    if text_lower.endswith('?') or any(text_lower.startswith(q + ' ') for q in QUESTION_STARTERS) or "yaar" in text_lower or "who is" in text_lower:
        return "QUESTION"
    
    # Check if opinion
    if any(marker in text_lower for marker in OPINION_MARKERS):
        return "OPINION"
        
    return "FACTUAL_CLAIM"

def normalize_text(text: str) -> str:
    """
    Normalizes Tanglish / Tamil or English mixed text internally
    """
    text_clean = text.strip()
    # Normalize common Tanglish political phrases
    text_clean = re.sub(r'\btamilnadu\b', 'Tamil Nadu', text_clean, flags=re.IGNORECASE)
    text_clean = re.sub(r'\bcm\b', 'Chief Minister', text_clean, flags=re.IGNORECASE)
    text_clean = re.sub(r'\byaar\b', 'who', text_clean, flags=re.IGNORECASE)
    return text_clean

def extract_entities_and_claims(text: str):
    """
    Extracts entities (PERSON, POSITION, LOCATION, YEAR, EVENT) and Claim Triplets
    """
    text_lower = text.lower()
    
    extracted_entities = {}
    
    # Extract Person
    found_person = None
    for key, val in PEOPLE.items():
        if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
            found_person = val
            break
    if found_person:
        extracted_entities["PERSON"] = found_person

    # Extract Position
    found_position = None
    for key, val in POSITIONS.items():
        if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
            found_position = val
            break
    if found_position:
        extracted_entities["GOVERNMENT_POSITION"] = found_position

    # Extract Location
    found_location = None
    for key, val in LOCATIONS.items():
        if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
            found_location = val
            break
    if found_location:
        extracted_entities["LOCATION"] = found_location

    # Extract Year
    year_match = re.search(r'\b(19\d\d|20\d\d)\b', text)
    if year_match:
        extracted_entities["YEAR"] = int(year_match.group(1))

    # Extract Event
    if "world cup" in text_lower or "cricket" in text_lower:
        extracted_entities["EVENT"] = "Cricket World Cup"

    # Construct Triplet
    subject = extracted_entities.get("PERSON") or extracted_entities.get("EVENT") or "Unknown"
    relation = "is " + (extracted_entities.get("GOVERNMENT_POSITION") or "related to") if "GOVERNMENT_POSITION" in extracted_entities else "claimed"
    obj = extracted_entities.get("LOCATION") or extracted_entities.get("YEAR") or "Unknown"
    
    claim_triplet = {
        "subject": subject,
        "relation": relation,
        "object": obj
    }
    
    return extracted_entities, claim_triplet
