import streamlit as st

def scanner_box():
    """
    Neon glowing scan box with proper container wrapping.
    """
    
    with st.container():
        st.markdown("""
        <style>
            .scan-wrapper {
                padding: 30px;
                border-radius: 22px;
                margin-top: 20px;
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: 0 0 25px rgba(126,78,255,0.35);
                backdrop-filter: blur(12px);
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='scan-wrapper'>", unsafe_allow_html=True)

        url = st.text_input("Enter URL to scan", placeholder="https://example.com", key="scanurl_fixed")
        scan_btn = st.button("Scan", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if scan_btn and url.strip():
            return url.strip()
        return None
