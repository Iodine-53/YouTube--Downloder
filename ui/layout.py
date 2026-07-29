import streamlit as st


def setup_page_config():
    st.set_page_config(
        page_title="YouTube Downloader",
        page_icon="📥",
        layout="centered",
        initial_sidebar_state="collapsed",
    )


def inject_custom_css():
    st.markdown("""
    <style>
    div[data-testid="stDecoration"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .video-card {
        background: var(--background-color);
        border: 1px solid var(--secondary-background-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .video-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-color);
        margin: 0.5rem 0;
        line-height: 1.4;
    }
    .video-meta {
        color: var(--text-color-muted, #888);
        font-size: 0.9rem;
    }
    div[data-testid="stImage"] img {
        border-radius: 8px;
    }
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    .header-title {
        text-align: center;
        margin-bottom: 0.25rem;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-color);
    }
    .header-subtitle {
        text-align: center;
        color: var(--text-color-muted, #888);
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .footer-note {
        text-align: center;
        color: var(--text-color-muted, #888);
        font-size: 0.8rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--secondary-background-color);
    }
    .size-warning {
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid var(--error-color, #ff4757);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--error-color, #ff4757);
    }
    .error-box {
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid var(--error-color, #ff4757);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--error-color, #ff4757);
    }
    .success-box {
        background: rgba(46, 204, 113, 0.1);
        border: 1px solid var(--success-color, #2ecc71);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--success-color, #2ecc71);
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("<div class='header-title'>📥 YouTube Downloader</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='header-subtitle'>"
        "Paste a YouTube link to fetch video info, select quality, and download."
        "</div>",
        unsafe_allow_html=True,
    )


def render_footer_note():
    st.markdown(
        "<div class='footer-note'>Supports public YouTube videos only.</div>",
        unsafe_allow_html=True,
    )
