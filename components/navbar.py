import streamlit as st

def navbar(items, active_key, on_select):
    """
    Clean, modern navbar rendering ONLY once.
    Uses pure HTML buttons inside <form>, no duplicate Streamlit widgets.
    """

    st.markdown("""
    <style>
        .navbar-container {
            display: flex;
            justify-content: center;
            gap: 18px;
            margin: 25px 0 35px 0;
        }

        .nav-btn {
            padding: 9px 26px;
            border-radius: 14px;
            font-weight: 500;
            font-size: 15px;
            cursor: pointer;
            color: #cdd1eb;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(6px);
            transition: all 0.25s ease;
        }

        .nav-btn:hover {
            color: white;
            border-color: rgba(255,255,255,0.25);
        }

        .nav-active {
            background: linear-gradient(90deg,#7b5bff,#5be4ff);
            color: white !important;
            border: none !important;
            box-shadow: 0 0 14px rgba(91,228,255,0.35);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='navbar-container'>", unsafe_allow_html=True)

    for label, key in items:
        active_class = "nav-active" if key == active_key else ""

        # forms with GET preserve Streamlit flow and do NOT duplicate elements
        st.markdown(
            f"""
            <form action="/" method="get">
                <input type="hidden" name="page" value="{key}">
                <button class="nav-btn {active_class}" type="submit">{label}</button>
            </form>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # update page from query param
    qp = st.query_params
    if "page" in qp:
        on_select(qp["page"])
