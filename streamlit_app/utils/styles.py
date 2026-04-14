"""
styles.py
─────────────────────────────────────────────────────────────────────────────
Single source of truth for application-wide CSS.
Import and call inject_global_css() at the top of every page's show() function.

Color variables are intentionally minimal and reference the theme palette
defined in config.toml so they stay consistent without duplication.
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st

_CSS = """
<style>
/* ── Reset / Base ─────────────────────────────────────────────────────────── */
#MainMenu, footer, header          { visibility: hidden; }
[data-testid="stToolbar"]          { display: none; }
[data-testid="stAppViewContainer"] { padding-top: 1.5rem; }

/* ── Typography ──────────────────────────────────────────────────────────── */
h1, h2, h3 { letter-spacing: -0.02em; font-weight: 600; }

/* ── Page header block ───────────────────────────────────────────────────── */
.page-header {
    text-align    : center;
    padding       : 2.5rem 1.5rem 2rem;
    margin-bottom : 2rem;
    border-radius : 12px;
    border        : 1px solid rgba(255,255,255,0.07);
    background    : rgba(255,255,255,0.02);
}
.page-header h1 {
    font-size   : 2.2rem;
    font-weight : 700;
    color       : #d4d8e8;
    margin      : 0 0 0.4rem;
}
.page-header p  { color: #7a8099; font-size: 1rem; margin: 0; }

/* ── Content cards ───────────────────────────────────────────────────────── */
.card {
    background    : rgba(255,255,255,0.03);
    border        : 1px solid rgba(255,255,255,0.07);
    border-radius : 10px;
    padding       : 1.5rem 1.75rem;
    margin-bottom : 1.25rem;
}
.card h3 {
    font-size     : 1rem;
    font-weight   : 600;
    color         : #4f8ef7;
    margin        : 0 0 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.card p  { color: #b0b6cc; line-height: 1.65; margin: 0.25rem 0; }

/* ── Section label inside forms ──────────────────────────────────────────── */
.section-label {
    font-size     : 0.75rem;
    font-weight   : 600;
    color         : #4f8ef7;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin        : 1.5rem 0 0.6rem;
    border-bottom : 1px solid rgba(79,142,247,0.2);
    padding-bottom: 0.35rem;
}

/* ── Result highlight card ───────────────────────────────────────────────── */
.result-card {
    background    : rgba(79,142,247,0.06);
    border        : 1px solid rgba(79,142,247,0.25);
    border-radius : 12px;
    padding       : 2rem;
    margin-bottom : 1.75rem;
    text-align    : center;
}
.result-card .cluster-label {
    font-size   : 1.6rem;
    font-weight : 700;
    color       : #d4d8e8;
    margin      : 0 0 0.35rem;
}
.result-card .tagline {
    font-size : 0.95rem;
    color     : #7a8099;
    margin    : 0 0 1rem;
}
.result-card .description {
    font-size   : 0.9rem;
    color       : #b0b6cc;
    line-height : 1.7;
    text-align  : left;
    margin      : 0;
}

/* ── Score bar ───────────────────────────────────────────────────────────── */
.score-row  { display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; }
.score-name { font-size: 0.8rem; color: #7a8099; width: 140px; flex-shrink: 0; }
.score-bar-track {
    flex          : 1;
    height        : 6px;
    background    : rgba(255,255,255,0.08);
    border-radius : 999px;
    overflow      : hidden;
}
.score-bar-fill {
    height        : 100%;
    border-radius : 999px;
    background    : #4f8ef7;
    transition    : width 0.4s ease;
}
.score-val { font-size: 0.8rem; color: #d4d8e8; width: 38px; text-align: right; }

/* ── Recommendation list ─────────────────────────────────────────────────── */
.rec-item {
    display       : flex;
    gap           : 0.6rem;
    padding       : 0.45rem 0;
    border-bottom : 1px solid rgba(255,255,255,0.04);
    font-size     : 0.88rem;
    color         : #b0b6cc;
    line-height   : 1.5;
}
.rec-item:last-child { border-bottom: none; }
.rec-bullet { color: #4f8ef7; flex-shrink: 0; margin-top: 2px; }

/* ── Priority badge ──────────────────────────────────────────────────────── */
.priority-badge {
    display       : inline-block;
    font-size     : 0.7rem;
    font-weight   : 600;
    padding       : 0.2rem 0.6rem;
    border-radius : 999px;
    margin-bottom : 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.priority-high     { background: rgba(239,68,68,0.15);  color: #f87171; }
.priority-medium   { background: rgba(234,179,8,0.15);  color: #facc15; }
.priority-low      { background: rgba(34,197,94,0.15);  color: #4ade80; }

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
    text-align : center;
    color      : #3d4259;
    padding    : 2.5rem 0 1rem;
    font-size  : 0.8rem;
}
</style>
"""


def inject_global_css() -> None:
    """Inject shared CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)