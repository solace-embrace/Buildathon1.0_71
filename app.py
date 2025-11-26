#===== app.py =====
import streamlit as st
import os
from datetime import datetime
from components.navbar import navbar
from components.header import header
from components.scanner_box import scanner_box
from components.result_card import result_card
from components.threat_analysis import threat_analysis
from components.features_section import features_section
from components.footer import footer
from utils.analyzer import analyze_url
import pandas as pd

# -------- TIME AGO (No external library needed) --------
def time_ago(timestamp_str):
    """
    Converts YYYY-MM-DD HH:MM:SS into '5 min ago', '2 hours ago', etc.
    Pure Python implementation.
    """
    now = datetime.now()
    past = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    diff = now - past
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        mins = int(seconds // 60)
        return f"{mins} min ago"
    elif seconds < 86400:
        hrs = int(seconds // 3600)
        return f"{hrs} hour ago" if hrs == 1 else f"{hrs} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day ago" if days == 1 else f"{days} days ago"


# Custom CSS
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="PhishShield",
    page_icon="🛡️",
    layout="centered"
)

# Ensure data dir and history file exists
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/history.csv"):
    with open("data/history.csv", "w") as f:
        f.write("url,verdict,confidence,timestamp\n")

def append_history(url, verdict, confidence):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f'"{url}",{verdict},{confidence},{ts}\n'
    with open("data/history.csv", "a") as f:
        f.write(row)

def load_history():
    try:
        return pd.read_csv("data/history.csv")
    except Exception:
        return pd.DataFrame(columns=["url","verdict","confidence","timestamp"])

if "page" not in st.session_state:
    st.session_state["page"] = "scanner"

def set_page(page):
    st.session_state["page"] = page

navbar(
    items=[("Scanner", "scanner"), ("Analytics", "analytics")],
    on_select=set_page,
    active_key=st.session_state['page']
)

if st.session_state["page"] == "scanner":
    header()
    url = scanner_box()
    if url:
        with st.spinner("Analyzing..."):
            verdict, confidence, reasons, features, explanation = analyze_url(url)
            append_history(url, verdict, confidence)
            result_card(verdict, confidence, explanation)
            features_section(reasons, features)
            threat_analysis(verdict, confidence)
# ================= ANALYTICS PAGE =======================
elif st.session_state["page"] == "analytics":
    
    st.markdown("<h2 class='analytics-header'>Analytics & Stats</h2>", unsafe_allow_html=True)
    
    history_df = load_history()

    if history_df.empty:
        st.info("No scans yet. Run your first scan from the Scanner tab!")
    else:
        
        # -------- WEEKLY SCAN ACTIVITY (FAKE SAMPLE FOR NOW) -------
        import numpy as np
        import pandas as pd
        
        st.markdown("### Weekly Scan Activity")
        
        weekly_data = pd.DataFrame({
            "Legitimate": np.random.randint(900, 2500, 7),
            "Phishing": np.random.randint(50, 300, 7)
        }, index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

        st.bar_chart(weekly_data)

        st.markdown("---")

        # -------- THREAT DISTRIBUTION (REAL COUNTS) --------
        st.markdown("### Threat Distribution")

        import matplotlib.pyplot as plt

        verdict_counts = history_df["verdict"].value_counts()

        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(
            verdict_counts,
            labels=verdict_counts.index,
            autopct="%1.1f%%",
            colors=["#00ff9c", "#ff4d6d", "#ffcc00"]
        )
        ax.set_title("")
        st.pyplot(fig)

        st.markdown("---")

        # -------- RECENT THREATS TABLE (BEAUTIFUL FORMAT) --------
        st.markdown("### Recent Threats Detected")

        styled_df = history_df.copy()

        # Type column (phishing/suspicious/safe)
        styled_df["Type"] = styled_df["verdict"].apply(
            lambda v: "Phishing" if v=="dangerous" 
                      else "Suspicious" if v=="suspicious" 
                      else "Legitimate"
        )

        # Risk Level
        styled_df["Risk Level"] = styled_df["verdict"].apply(
            lambda v: "High" if v=="dangerous"
                      else "Medium" if v=="suspicious"
                      else "Low"
        )

        # Detected (time ago)
        styled_df["Detected"] = styled_df["timestamp"].apply(time_ago)


        # Final table
        final_df = styled_df[["url","Type","Risk Level","Detected"]]
        final_df.columns = ["Domain","Type","Risk","Detected"]

        st.dataframe(
            final_df,
            hide_index=True,
            use_container_width=True
        )


footer()