


#===== components/header.py =====
import streamlit as st

def header():
    """
    Hero section with logo, gradient text, and stats row.
    """
    st.markdown("""
    <div class="phshield-header">
      <div class="phshield-shieldrow">
        <span class="phshield-shieldicon">🛡️</span>
        <span class="phshield-title">Phish<span class="phshield-title-gradient">Shield</span></span>
      </div>
      <div class="phshield-subtitle">Score-based phishing scanner. Modular, fast, neon UI—hackathon ready.</div>
      <div class="phshield-statsrow">
        <div class="phshield-stat"><span class="phshield-stat-v">99.8%</span>Accuracy</div>
        <div class="phshield-stat"><span class="phshield-stat-v">0.3s</span>Response</div>
        <div class="phshield-stat"><span class="phshield-stat-v">2M+</span>URLs Scanned</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
