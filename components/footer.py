
#===== components/footer.py =====
import streamlit as st

def footer():
    st.markdown("""
    <div class='phshield-footer'>
      <span>© 2024 PhishShield. Built during hackathon event. <i>AI optional.</i></span>
    </div>
    """, unsafe_allow_html=True)