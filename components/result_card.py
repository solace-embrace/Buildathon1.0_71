
#===== components/result_card.py =====
import streamlit as st

def verdict_badge(verdict, confidence):
    label = ""
    klass = ""
    if verdict == "dangerous":
        label = "Dangerous"
        klass = "badge-danger"
    elif verdict == "suspicious":
        label = "Suspicious"
        klass = "badge-suspicious"
    elif verdict == "low_risk":
        label = "Low Risk"
        klass = "badge-lowrisk"
    else:
        label = "Safe"
        klass = "badge-safe"
    return f"<span class='phshield-badge {klass}'>{label}</span>"

def result_card(verdict, confidence, explanation):
    """
    Result glass card with large verdict badge, confidence, description.
    """
    st.markdown(f"""
    <div class="phshield-card phshield-resultcard">
      <div class="phshield-result-row">
        <span class="phshield-result-heading">Result</span>
        {verdict_badge(verdict, confidence)}
      </div>
      <div class="phshield-confidence">Confidence: 
        <span class="phshield-confidence-val conf-{verdict}">{confidence}%</span>
      </div>
      <div class="phshield-explanation">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)