#===== components/result_card.py =====
import streamlit as st
import html


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
    Premium result card with verdict badge, confidence score,
    and a highlighted AI explanation block.
    """
    # Escape explanation to prevent raw HTML being shown or interpreted.
    safe_explanation = html.escape(explanation).replace("\n", "<br>")

    st.markdown(f"""
    <div class="phshield-card phshield-resultcard">

        <!-- RESULT ROW -->
        <div class="phshield-result-row">
            <span class="phshield-result-heading">Result</span>
            {verdict_badge(verdict, confidence)}
        </div>

        <!-- CONFIDENCE -->
        <div class="phshield-confidence">
            Confidence:
            <span class="phshield-confidence-val conf-{verdict}">
                {confidence}%
            </span>
        </div>

        <!-- AI EXPLANATION BLOCK -->
        <div class="phshield-ai-box">
            <div class="phshield-ai-title">🧠 AI Explanation</div>
            <div class="phshield-ai-text">{safe_explanation}</div>
        </div>

    </div>
    """, unsafe_allow_html=True)
