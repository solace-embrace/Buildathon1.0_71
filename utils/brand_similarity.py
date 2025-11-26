from difflib import SequenceMatcher

# Popular brands commonly impersonated
BRANDS = [
    "google", "paypal", "amazon", "facebook", "microsoft", 
    "apple", "instagram", "whatsapp", "netflix", "linkedin"
]

def normalize(domain: str) -> str:
    """
    Normalize domain by replacing look-alike characters used in phishing.
    Example: g00gle → google
    """
    replacements = {
        "0": "o",
        "1": "l",
        "3": "e",
        "5": "s",
        "@": "a",
        "-": ""
    }

    for bad, good in replacements.items():
        domain = domain.replace(bad, good)

    return domain.lower()

def compute_brand_similarity(domain: str):
    """
    Compute similarity between domain and known brands.
    Returns: (best_score, best_match_brand)
    """

    domain_norm = normalize(domain)

    best_score = 0
    best_brand = ""

    for brand in BRANDS:
        score = SequenceMatcher(None, domain_norm, brand).ratio()

        if score > best_score:
            best_score = score
            best_brand = brand

    return best_score, best_brand
