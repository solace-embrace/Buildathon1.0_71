# ========================= app.py =========================

import streamlit as st
import os
import html
from datetime import datetime

from components.navbar import navbar
from components.header import header
from components.scanner_box import scanner_box
from components.result_card import result_card
from components.features_section import features_section
from components.footer import footer
from utils.analyzer import analyze_url

import pandas as pd


# ---------------- TIME AGO ----------------
def time_ago(timestamp_str):
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


# ---------------- LOAD CSS ----------------
try:
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("Error: styles/theme.css not found.")


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PhishShield",
    page_icon="🥀",
    layout="centered",
)


# ---------------- HISTORY FILE ----------------
os.makedirs("data", exist_ok=True)

if not os.path.exists("data/history.csv"):
    with open("data/history.csv", "w") as f:
        f.write("url,verdict,confidence,timestamp\n")


def append_history(url, verdict, confidence):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data/history.csv", "a") as f:
        f.write(f'"{url}",{verdict},{confidence},{ts}\n')


def load_history():
    try:
        return pd.read_csv("data/history.csv")
    except:
        return pd.DataFrame(columns=["url", "verdict", "confidence", "timestamp"])


# ---------------- NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "scanner"


def set_page(page):
    st.session_state["page"] = page


navbar(
    items=[("Scanner", "scanner"), ("Analytics", "analytics")],
    on_select=set_page,
    active_key=st.session_state["page"],
)


# ============================================================
#                       SCANNER PAGE
# ============================================================
if st.session_state["page"] == "scanner":

    header()

    # ---------------- AI TOGGLE ----------------
    st.markdown("### 😔 AI Explanation")

    if "use_ai" not in st.session_state:
        st.session_state.use_ai = False

    st.session_state.use_ai = st.toggle(
        "Enable AI Explanation (Optional)",
        value=st.session_state.use_ai,
        key="ai_toggle",
    )

    use_ai = st.session_state.use_ai

    # ---------------- URL INPUT ----------------
    url = scanner_box()

    if url:
        with st.spinner("Analyzing URL..."):
            verdict, confidence, reasons, features, explanation = analyze_url(url, use_ai)
            append_history(url, verdict, confidence)

        # ---------------- THREAT SCORE BAR ----------------
        if verdict == "safe":
            glow = "#22c55e"
            bar_color = "#22c55e"
            bg = "rgba(34,197,94,0.15)"
        elif verdict == "suspicious":
            glow = "#facc15"
            bar_color = "#facc15"
            bg = "rgba(250,204,21,0.15)"
        else:
            glow = "#ef4444"
            bar_color = "#ef4444"
            bg = "rgba(239,68,68,0.15)"

        st.markdown(
            f"""
            <div style="
                background:{bg};
                padding:22px;
                border-radius:18px;
                border:1px solid {glow};
                box-shadow:0 0 22px {glow};
                margin-top:20px;
                margin-bottom:25px;
            ">
                <div style="
                    width:100%;
                    background:#111;
                    height:14px;
                    border-radius:10px;
                    overflow:hidden;
                ">
                    <div style="
                        width:{confidence}%;
                        height:14px;
                        background:{bar_color};
                        border-radius:10px;
                    "></div>
                </div>

                <div style="
                    text-align:center;
                    margin-top:12px;
                    color:white;
                    font-size:20px;
                    font-weight:700;
                ">
                    {verdict.title()} Threat Score: {confidence}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ---------------- EXPLANATION BOX ----------------
        glow_color = "#c084fc" if use_ai else "#94a3b8"
        bg_color = "rgba(138,43,226,0.15)" if use_ai else "rgba(148,163,184,0.12)"
        title_text = "🔮 AI Explanation" if use_ai else "📝 Rule-Based Explanation"

        # raw text
        raw_body = explanation if use_ai else "\n".join(reasons)

        # Escape only HTML brackets, keep quotes natural
        safe_text = (
            raw_body.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>")
        )


        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:14px;
                margin-bottom:30px;
                border:1px solid {glow_color};
                background:{bg_color};
                box-shadow:0 0 18px {glow_color};
            ">
                <div style="
                    color:{glow_color};
                    font-size:20px;
                    font-weight:700;
                    margin-bottom:10px;
                ">
                    {title_text}
                </div>

                <div style="
                    color:#e2e8f0;
                    font-size:16px;
                    line-height:1.55;
                    white-space:normal;
                ">
                    {safe_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ---------------- RESULT CARD + FEATURES ----------------
        result_card(verdict, confidence, explanation)
        features_section(reasons, features)


# ============================================================
#                       ANALYTICS PAGE
# ============================================================
elif st.session_state["page"] == "analytics":

    st.markdown("<h2 class='analytics-header'>Analytics & Stats</h2>", unsafe_allow_html=True)

    history_df = load_history()

    if history_df.empty:
        st.info("No scans yet. Run your first scan from the Scanner tab!")

    else:
        import numpy as np
        import matplotlib.pyplot as plt

        st.markdown("### Weekly Scan Activity")

        weekly_data = pd.DataFrame(
            {
                "Legitimate": np.random.randint(900, 2500, 7),
                "Phishing": np.random.randint(50, 300, 7),
            },
            index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        )

        st.bar_chart(weekly_data)

        st.markdown("---")
        st.markdown("### Threat Distribution")

        verdict_counts = history_df["verdict"].value_counts()

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            verdict_counts,
            labels=verdict_counts.index,
            autopct="%1.1f%%",
            colors=["#22c55e", "#ef4444", "#facc15"],
        )
        st.pyplot(fig)

        st.markdown("---")
        st.markdown("### Recent Threats Detected")

        styled_df = history_df.copy()

        styled_df["Type"] = styled_df["verdict"].apply(
            lambda v: "Phishing" if v == "dangerous" else "Suspicious" if v == "suspicious" else "Legitimate"
        )

        styled_df["Risk Level"] = styled_df["verdict"].apply(
            lambda v: "High" if v == "dangerous" else "Medium" if v == "suspicious" else "Low"
        )

        styled_df["Detected"] = styled_df["timestamp"].apply(time_ago)

        final_df = styled_df[["url", "Type", "Risk Level", "Detected"]]
        final_df.columns = ["Domain", "Type", "Risk", "Detected"]

        st.dataframe(final_df, hide_index=True, use_container_width=True)


# ---------------- FOOTER ----------------
footer()

# ========================= END app.py =========================
