

#===== utils/analyzer.py =====
import os
import random
from utils.brand_similarity import compute_brand_similarity
from utils.url_helpers import extract_domain, extract_path, has_raw_ip
import openai

PHISH_KEYWORDS = [
    "login", "verify", "secure", "update", "account", "password", "paypal",
    "amazon", "bank"
]
SUSPICIOUS_TLDS = [
    "xyz", "top", "gq", "zip", "ml", "work", "co.vu", "ru"
]
SHORTENERS = [
    "bit.ly", "t.co", "tinyurl", "goo.gl"
]

def analyze_url(url):
    """
    Main entry: returns (verdict, confidence, reasons, features, explanation)
    """
    # Features extraction
    domain = extract_domain(url)
    path = extract_path(url)
    features = {}
    reasons = []
    score = 0

    # 1. High-Risk Indicators
    if has_raw_ip(domain):
        score += 50
        reasons.append("URL uses a raw IP address (no domain).")
        features['ip_in_url'] = True
    else:
        features['ip_in_url'] = False

    brand_score, brand_name = compute_brand_similarity(domain)
    features['brand_similarity'] = f"{brand_score:.2f}"
    features['impersonated_brand'] = brand_name if brand_score > 0.7 else ''
    if brand_score > 0.85:
        score += 40
        reasons.append(f"Domain closely matches popular brand: '{brand_name}' ({brand_score:.2f})")

    tld = domain.split(".")[-1].lower()
    for badtld in SUSPICIOUS_TLDS:
        if tld == badtld or domain.endswith("." + badtld):
            score += 40
            reasons.append(f"Suspicious TLD found ({tld}).")
            features['suspicious_tld'] = tld

    for kw in PHISH_KEYWORDS:
        if kw in domain.lower() or kw in path.lower():
            score += 35
            reasons.append(f"Phishing keyword '{kw}' detected in URL.")
            features[f'kw_{kw}'] = True

    # 2. Medium Indicators
    digit_ct = sum(c.isdigit() for c in domain)
    if digit_ct >= 3:
        score += 15
        reasons.append("Domain includes 3 or more digits.")
        features['digits'] = digit_ct

    hyphen_ct = domain.count("-")
    if hyphen_ct >=2:
        score += 15
        reasons.append("Domain contains 2 or more hyphens.")
        features['hyphens'] = hyphen_ct

    if len(path) > 50:
        score += 10
        reasons.append("Path is very long (>50 chars).")
        features['path_length'] = len(path)

    if any(param in url.lower() for param in ["url=", "redirect=", "next="]):
        score += 15
        reasons.append("Redirect parameter detected in URL.")
        features['redirect_param'] = True

    # 3. Shortener
    if any(short in domain for short in SHORTENERS):
        score += 25
        reasons.append("Known URL shortener service.")
        features['is_shortener'] = True
    else:
        features['is_shortener'] = False

    # Compute final verdict, confidence
    features["score"] = score
    if score <= 9:
        verdict = "safe"
        confidence = 95
    elif score <= 39:
        verdict = "low_risk"
        confidence = 60
    elif score <= 69:
        verdict = "suspicious"
        confidence = random.randint(75, 89)
    else:
        verdict = "dangerous"
        confidence = 94

    # AI Explanation logic
    explanation = ""
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            openai.api_key = openai_key
            prompt = (
                f"You are a security analyst. Explain—in 2-3 sentences—why the following URL got verdict '{verdict}' with confidence {confidence}%. "
                f"Reasons were: {', '.join(reasons)}"
            )
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=56,
                temperature=0.32
            )
            explanation = resp.choices[0].text.strip()
        except Exception:
            explanation = "\n".join(reasons)
    else:
        explanation = "\n".join(reasons)
    return verdict, confidence, reasons, features, explanation