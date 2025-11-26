
#===== components/features_section.py =====
import streamlit as st

def features_section(reasons, features):
    """
    Visual section: list of triggered detection mechanisms, plus features summary.
    """
    st.markdown("""
    <div class="phshield-card phshield-fsec">
      <span class="phshield-ftr-title">Why this verdict?</span>
      <ul class="phshield-ftrlist">
    """, unsafe_allow_html=True)
    if reasons:
        for reason in reasons:
            st.markdown(f"<li>{reason}</li>", unsafe_allow_html=True)
    else:
        st.markdown("<li>No strong indicators detected.</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    # Feature dump (compact)
    st.markdown("<div class='phshield-ftrstats'>", unsafe_allow_html=True)
    for k,v in features.items():
        st.markdown(f"<div class='phshield-ftrstat'><b>{k}</b>: <span>{v}</span></div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
