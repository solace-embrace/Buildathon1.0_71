

===== README.md =====
# PhishShield

**Modular Score-based Phishing Detection | Neon UI | Hackathon Edition**

![shield logo](https://emojicdn.elk.sh/%F0%9F%9B%A1%EF%B8%8F)

## 🚀 Features

- **Score-Based Phishing Engine** with confidence, strict rules, and explainability.
- **Glassmorphism/Neon Dark UI** & navbar.
- **Brand impersonation detection** (string similarity)
- **Auto-detect risky TLDs, keywords, digits, hyphens, redirect params, URL shorteners**
- **Analytics**: verdict distribution, bar/pie charts, average confidence.
- **2M+ URLs Scanned, 99.8% Accuracy, 0.3s Response** (demo style).
- **Optionally**: AI explanations (if `OPENAI_API_KEY` set).

## 📥 How To Run

```bash
git clone <repo>
cd PhishShield
pip install -r requirements.txt
streamlit run app.py
```

- Requires: Python 3.8+, Streamlit, pandas, matplotlib
- Optional: OpenAI for natural explanations

## 🔐 Security/Disclaimer

- This tool provides a *rule-based* phishing risk analysis.
- Results are **demonstrative**—do not rely on this for real-world critical protection.
- **No URLs are ever sent to a third party unless you use the OpenAI API key.**
- AI explanations are optional.

---
_Built during hackathon event. AI optional._
