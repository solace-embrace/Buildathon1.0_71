import os
import random
from dotenv import load_dotenv

from utils.brand_similarity import compute_brand_similarity
from utils.url_helpers import extract_domain, extract_path, has_raw_ip

from groq import Groq

# Load .env file (so GROQ_API_KEY works locally & on cloud)
load_dotenv()

# --------------------------
# RULE-BASED CONFIG
# --------------------------
PHISH_KEYWORDS = [
    "login", "verify", "secure", "update", "account", "password",
    "paypal", "amazon", "bank"
]

SUSPICIOUS_TLDS = [
    "xyz", "top", "gq", "zip", "ml", "work", "co.vu", "ru"
]

SHORTENERS = ["bit.ly", "t.co", "tinyurl", "goo.gl"]


# --------------------------
# MAIN FUNCTION
# --------------------------
def analyze_url(url, use_ai=False):
    """
    Main entry: returns (verdict, confidence, reasons, features, explanation)
    """

    # --------------------------
    # FEATURE EXTRACTION
    # --------------------------
    domain = extract_domain(url)
    path = extract_path(url)

    features = {}
    reasons = []
    score = 0

    # 1. High-risk: Raw IP
    if has_raw_ip(domain):
        score += 50
        reasons.append("URL uses a raw IP address (no domain).")
        features['ip_in_url'] = True
    else:
        features['ip_in_url'] = False

    # 2. Brand impersonation
    brand_score, brand_name = compute_brand_similarity(domain)
    features['brand_similarity'] = round(brand_score, 2)
    features['impersonated_brand'] = brand_name if brand_score >= 0.70 else ""

    if brand_score >= 0.90:
        score += 40
        reasons.append(
            f"Domain strongly resembles popular brand '{brand_name}' (similarity {brand_score:.2f})."
        )
    elif brand_score >= 0.75:
        score += 25
        reasons.append(
            f"Domain appears similar to brand '{brand_name}' (possible impersonation, {brand_score:.2f})."
        )

    # 3. Suspicious TLD
    tld = domain.split(".")[-1].lower()
    for badtld in SUSPICIOUS_TLDS:
        if tld == badtld or domain.endswith("." + badtld):
            score += 40
            reasons.append(f"Suspicious TLD found ({tld}).")
            features['suspicious_tld'] = tld
            break # Found one, move on

    # 4. Keyword presence
    for kw in PHISH_KEYWORDS:
        if kw in domain.lower() or kw in path.lower():
            score += 35
            reasons.append(f"Phishing keyword '{kw}' detected in URL.")
            features[f'kw_{kw}'] = True

    # 5. Medium indicators
    digit_ct = sum(c.isdigit() for c in domain)
    if digit_ct >= 3:
        score += 15
        reasons.append("Domain includes 3 or more digits.")
        features['digits'] = digit_ct

    hyphen_ct = domain.count("-")
    if hyphen_ct >= 2:
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

    # 6. Shorteners
    if any(short in domain for short in SHORTENERS):
        score += 25
        reasons.append("Known URL shortener service.")
        features['is_shortener'] = True
    else:
        features['is_shortener'] = False

    # --------------------------
    # VERDICT & CONFIDENCE
    # --------------------------
    features["score"] = score

    # Define confidence based on score
    if score <= 9:
        verdict = "safe"
        confidence = 95 # High confidence for safe

    elif score <= 39:
        verdict = "low_risk"
        confidence = 60 # Lower confidence for low risk

    elif score <= 69:
        verdict = "suspicious"
        confidence = random.randint(75, 89) # Mid-high confidence for suspicious

    else:
        verdict = "dangerous"
        confidence = 94 # High confidence for dangerous

    # --------------------------
    # AI EXPLANATION (GROQ)
    # --------------------------
    groq_key = os.getenv("GROQ_API_KEY")
    
    # Initialize explanation with rule-based reasons (fallback)
    explanation = "\n".join(reasons)

    # If AI disabled or key missing → return rule-based explanation
    if not use_ai or not groq_key:
        return verdict, confidence, reasons, features, explanation

    # If AI enabled and key available → generate explanation
    try:
        client = Groq(api_key=groq_key)

        # Prepare reasons text for the LLM
        reasons_text = "\n".join(f"- {r}" for r in reasons) if reasons else "None."

        prompt = f"""
You are a concise, helpful cybersecurity expert. Explain in 2–4 short sentences why this URL is classified as '{verdict}' with {confidence}% confidence.

URL: {url}

Signals detected:
{reasons_text}

Provide ONLY the explanatory text. DO NOT include any introductory phrases, titles, or quotation marks around the final answer.
"""

        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=180
        )

        explanation = resp.choices[0].message.content.strip()
        
        # FIX: Aggressively strip leading/trailing quotes and common LLM boilerplate/markdown wrappers
        explanation = explanation.strip('"`')
        if explanation.startswith("text: "): # Some models prefix with 'text: '
            explanation = explanation[6:]
        
    except Exception as e:
        # On failure, fall back to the simple rule-based explanation
        explanation = "\n".join(reasons)

    # Final return
    return verdict, confidence, reasons, features, explanation