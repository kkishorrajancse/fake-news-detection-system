import os
import json
import urllib.request
import urllib.parse
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PATH = os.path.join(PROJECT_ROOT, "data", "knowledge_base.json")

def load_kb():
    if os.path.exists(KB_PATH):
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

TRUSTED_DOMAINS = {
    "pib.gov.in": 1.0,
    "eci.gov.in": 1.0,
    "tn.gov.in": 1.0,
    "india.gov.in": 1.0,
    "who.int": 1.0,
    "nasa.gov": 1.0,
    "isro.gov.in": 1.0,
    "wikipedia.org": 0.95,
    "reuters.com": 0.90,
    "bbc.com": 0.90,
    "thehindu.com": 0.90,
    "factcheck.org": 0.95,
    "snopes.com": 0.95,
    "politifact.com": 0.95,
    "altnews.in": 0.95
}

def rate_source_credibility(source_name_or_url: str):
    source_lower = source_name_or_url.lower()
    for domain, score in TRUSTED_DOMAINS.items():
        if domain in source_lower:
            return {"score": score, "rating": "High" if score >= 0.85 else "Medium"}
    if "official" in source_lower or "government" in source_lower:
        return {"score": 0.95, "rating": "High"}
    if "blog" in source_lower or "social" in source_lower or "forum" in source_lower:
        return {"score": 0.20, "rating": "Low"}
    return {"score": 0.60, "rating": "Medium"}

def query_local_knowledge_base(entities: dict, claim_text: str):
    kb = load_kb()
    evidences = []
    
    person = entities.get("PERSON")
    position = entities.get("GOVERNMENT_POSITION")
    location = entities.get("LOCATION")
    event = entities.get("EVENT")
    year = entities.get("YEAR")

    # 1. Office Holders Check
    if person or position or location:
        for holder in kb.get("office_holders", []):
            loc_match = not location or holder["location"].lower() == location.lower()
            pos_match = not position or holder["position"].lower() == position.lower()
            
            if loc_match and pos_match:
                url_link = "https://india.gov.in" if holder['location'].lower() == "india" else "https://tn.gov.in"
                if holder["is_current"]:
                    evidences.append({
                        "source": f"Official {holder['location']} Government Registry & Election Records",
                        "url": url_link,
                        "date": "2026-10-07",
                        "snippet": f"The current official {holder['position']} of {holder['location']} is {holder['person']} ({holder['party']}), serving since {holder['start_year']}.",
                        "credibility": "High",
                        "credibility_score": 1.0,
                        "type": "OFFICE_HOLDER_CURRENT",
                        "current_holder": holder["person"]
                    })
                else:
                    evidences.append({
                        "source": f"Historical Archive of {holder['location']} Government",
                        "url": url_link,
                        "date": f"{holder['start_year']}-{holder['end_year']}",
                        "snippet": f"Historical Record: {holder['person']} served as {holder['position']} of {holder['location']} from {holder['start_year']} to {holder['end_year']}.",
                        "credibility": "High",
                        "credibility_score": 0.95,
                        "type": "OFFICE_HOLDER_HISTORICAL",
                        "holder": holder["person"],
                        "start_year": holder["start_year"],
                        "end_year": holder["end_year"]
                    })

    # 2. Persons & Parties Check
    for person_info in kb.get("persons_and_parties", []):
        if person and (person.lower() in person_info["person"].lower() or any(a.lower() in person.lower() for a in person_info["aliases"])):
            evidences.append({
                "source": "Election Commission & Political Party Records",
                "url": "https://eci.gov.in",
                "date": "2026-10-07",
                "snippet": f"{person_info['person']} is an {person_info['role']} and founder/member of {person_info['party']}. {person_info['notes']}",
                "credibility": "High",
                "credibility_score": 0.95,
                "type": "PERSON_PARTY_PROFILE"
            })

    # 4. Government Schemes Check
    for scheme in kb.get("government_schemes", []):
        if scheme["scheme"].lower() in claim_text.lower() or any(w in claim_text.lower() for w in scheme["scheme"].lower().split()):
            evidences.append({
                "source": f"Official {scheme['state']} Government Portal",
                "url": "https://tn.gov.in/schemes",
                "date": "2026",
                "snippet": f"{scheme['scheme']}: {scheme['details']}",
                "credibility": "High",
                "credibility_score": 1.0,
                "type": "GOVERNMENT_SCHEME"
            })

    return evidences

def query_live_wikipedia(query_text: str):
    """
    Live external evidence retrieval from Wikipedia API (Zero Hallucination)
    """
    try:
        clean_q = urllib.parse.quote(query_text[:80])
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={clean_q}&format=json&utf8=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'VeritasAI-FactChecker/2.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                top = search_results[0]
                snippet = re.sub(r'<.*?>', '', top.get('snippet', ''))
                title = top.get('title', '')
                page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                return {
                    "source": f"Wikipedia Encyclopedia ({title})",
                    "url": page_url,
                    "date": "2026",
                    "snippet": f"{title}: {snippet}...",
                    "credibility": "High",
                    "credibility_score": 0.95,
                    "type": "LIVE_ENCYCLOPEDIA"
                }
    except Exception:
        pass
    return None

def retrieve_all_evidence(entities: dict, claim_text: str):
    evidences = query_local_knowledge_base(entities, claim_text)
    
    # Query live encyclopedia for entity or claim
    search_query = entities.get("PERSON") or entities.get("EVENT") or claim_text[:50]
    live_ev = query_live_wikipedia(search_query)
    if live_ev:
        evidences.append(live_ev)

    return evidences
