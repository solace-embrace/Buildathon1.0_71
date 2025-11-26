


#===== components/threat_analysis.py =====
import streamlit as st

def threat_analysis(verdict, confidence):
    """
    Minimal chart or radial gauge - or visual based on verdict.
    """
    # This is a static look for now
    bar_color = {
        "dangerous": "#f5365c",
        "suspicious": "#faad14",
        "low_risk": "#faad14",
        "safe": "#00ff99"
    }[verdict]
    st.markdown(f"""
    <div class="phshield-card phshield-tavis" style="padding:2px 0 0 0;">
      <div class="phshield-tavis-barwrap">
        <div class="phshield-tavis-bar" style="width:{confidence}%;background:{bar_color};"></div>
      </div>
      <div class="phshield-tavis-label">{verdict.replace('_',' ').title()} Threat Score: <b>{confidence}%</b></div>
    </div>
    """, unsafe_allow_html=True)
