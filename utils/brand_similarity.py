#===== utils/brand_similarity.py =====
import difflib

COMMON_BRANDS = [
    "paypal", "amazon", "apple", "bankofamerica", "wellsfargo", "microsoft",
    "google", "facebook", "netflix", "chase", "dropbox", "instagram", "linkedin"
]

def compute_brand_similarity(domain):
    """
    Checks how similar domain is to major brands (ratio in 0–1), returns max_score, brand_name
    """
    base = domain.split(".")[0].lower().replace("-", "").replace("_","")
    max_score = 0.0
    best_brand = ""
    for brand in COMMON_BRANDS:
        sim = difflib.SequenceMatcher(None, base, brand).ratio()
        if sim > max_score:
            max_score = sim
            best_brand = brand
    return max_score, best_brand