import spacy
from utils import basic_sentiment, extract_emojis, POSITIVE_EMOJIS, NEGATIVE_EMOJIS

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


def analyze(text: str) -> dict:
    if not text or text.strip() == "":
        return {"mood": "neutral", "energy": "low"}
    
    vader_score = basic_sentiment(text)
    doc = nlp(text)
    
    for token in doc:
        if token.pos_ == "VERB" and token.lemma_ == "crush":
            children = [child for child in token.children if child.dep_ in ("dobj", "attr")]
            obj_texts = [child.text.lower() for child in children]
            
            if any("it" in obj for obj in obj_texts):
                return {"mood": "positive", "energy": "high"}
            
            if any(obj in ["me", "you", "us"] for obj in obj_texts):
                return {"mood": "negative", "energy": "high_stress"}
    
    emojis = extract_emojis(text)
    if emojis:
        pos_count = sum(1 for e in emojis if e in POSITIVE_EMOJIS)
        neg_count = sum(1 for e in emojis if e in NEGATIVE_EMOJIS)
        
        if neg_count > pos_count and neg_count > 0:
            return {"mood": "negative", "energy": "high_stress"}
        elif pos_count > neg_count and pos_count > 0:
            return {"mood": "positive", "energy": "high"}
    
    if vader_score > 0.1:
        energy = "high" if vader_score > 0.5 else "medium"
        return {"mood": "positive", "energy": energy}
    
    elif vader_score < -0.1:
        energy = "high_stress" if vader_score < -0.5 else "medium"
        return {"mood": "negative", "energy": energy}
    
    return {"mood": "neutral", "energy": "medium"}
