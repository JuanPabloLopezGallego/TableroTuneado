import os
import base64
import numpy as np
import streamlit as st
from PIL import Image
from openai import OpenAI
import openai
from streamlit_drawable_canvas import st_canvas

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title='Tablero Inteligente',
    page_icon='◆',
    layout='wide',
    initial_sidebar_state='collapsed',
)

# ═══════════════════════════════════════════════════════════════
# ESTILOS — BAUHAUS / CONSTRUCTIVISTA
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --bg:       #f2ede0;
        --surface:  #ffffff;
        --ink:      #0f0f0f;
        --ink-2:    #2a2a2a;
        --muted:    #6b6b5f;
        --line:     #d6cfb8;
        --red:      #e63946;
        --yellow:   #ffd400;
        --blue:     #1d4ed8;
    }

    /* ═══ BASE ═══ */
    html, body, [class*="css"], .stApp, button, input, textarea, select {
        font-family: 'Inter', sans-serif !important;
        color: var(--ink) !important;
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        color: var(--ink) !important;
    }

    /* ═══ FONDO CON RETÍCULA BAUHAUS ═══ */
    .stApp {
        background-color: var(--bg) !important;
        background-image:
            linear-gradient(rgba(15, 15, 15, 0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(15, 15, 15, 0.045) 1px, transparent 1px);
        background-size: 32px 32px;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1240px !important;
    }

    /* ═══ SIDEBAR ═══ */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 3px solid var(--ink) !important;
    }
    [data-testid="stSidebar"] * { color: var(--ink) !important; }

    .sb-head {
        background: var(--ink);
        color: #ffffff !important;
        padding: 0.9rem 1rem;
        margin: -1rem -1rem 1.5rem -1rem;
        position: relative;
        overflow: hidden;
    }
    .sb-head::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 36px;
        height: 36px;
        background: var(--yellow);
        clip-path: polygon(100% 0, 0 0, 100% 100%);
    }
    .sb-head .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--yellow) !important;
        font-weight: 700;
        display: block;
        margin-bottom: 0.3rem;
    }
    .sb-head .title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        letter-spacing: -0.02em;
        color: #ffffff !important;
        line-height: 1.1;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--red) !important;
        border-color: var(--ink) !important;
        border-width: 2px !important;
        border-radius: 0 !important;
        width: 16px !important;
        height: 16px !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
        background: var(--ink) !important;
        border-radius: 0 !important;
    }

    /* ═══ HEADER BANNER ═══ */
    .banner {
        background: var(--ink);
        color: #ffffff !important;
        padding: 0.85rem 1.4rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.25rem;
        border: 3px solid var(--ink);
        position: relative;
        overflow: hidden;
    }
    .banner::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 90px;
        background: repeating-linear-gradient(
            -45deg,
            var(--red) 0 12px,
            var(--ink) 12px 24px
        );
    }
    .banner-left {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        z-index: 1;
    }
    .banner-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        background: var(--yellow);
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .banner-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 700;
        color: #ffffff !important;
    }
    .banner-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #ffffff !important;
        font-weight: 500;
        z-index: 1;
        background: var(--ink);
        padding: 0.3rem 0.7rem;
        border: 1px solid var(--yellow);
    }
    .banner-meta b { color: var(--yellow) !important; }

    /* ═══ HERO CON GEOMETRÍA ═══ */
    .hero {
        display: grid;
        grid-template-columns: 90px 1fr auto;
        gap: 1.75rem;
        align-items: start;
        padding-bottom: 2rem;
        margin-bottom: 2.5rem;
        border-bottom: 3px solid var(--ink);
        position: relative;
    }

    /* Bloque geométrico a la izquierda */
    .hero-shape {
        position: relative;
        width: 90px;
        height: 120px;
    }
    .hero-shape .circle {
        position: absolute;
        top: 0;
        left: 0;
        width: 60px;
        height: 60px;
        background: var(--red);
        border-radius: 50%;
        border: 3px solid var(--ink);
    }
    .hero-shape .square {
        position: absolute;
        top: 40px;
        left: 30px;
        width: 55px;
        height: 55px;
        background: var(--yellow);
        border: 3px solid var(--ink);
        mix-blend-mode: multiply;
    }
    .hero-shape .triangle {
        position: absolute;
        bottom: 0;
        left: 5px;
        width: 0;
        height: 0;
        border-left: 28px solid transparent;
        border-right: 28px solid transparent;
        border-bottom: 45px solid var(--blue);
    }

    .hero-body { padding-top: 0.35rem; }
    .hero-eyebrow {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--ink);
        font-weight: 700;
        background: var(--yellow);
        padding: 0.35rem 0.7rem;
        border: 2px solid var(--ink);
        margin-bottom: 1rem;
        transform: rotate(-1.5deg);
        display: inline-block;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 3.5rem !important;
        line-height: 0.95 !important;
        letter-spacing: -0.045em !important;
        font-weight: 700 !important;
        margin: 0 0 1rem 0 !important;
        color: var(--ink) !important;
        text-transform: uppercase;
    }
    .hero h1 .blue {
        color: var(--blue) !important;
        font-weight: 700;
    }
    .hero h1 .red {
        color: var(--red) !important;
        font-weight: 700;
    }
    .hero h1 .underline {
        background: linear-gradient(transparent 60%, var(--yellow) 60%);
        padding: 0 0.15em;
    }
    .hero p {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--ink-2);
        margin: 0;
        max-width: 540px;
        font-weight: 400;
    }

    /* Tarjetas tipo "specs" a la derecha */
    .hero-specs {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        min-width: 200px;
    }
    .spec {
        background: var(--surface);
        border: 2px solid var(--ink);
        padding: 0.6rem 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        transition: transform 0.15s ease;
    }
    .spec:nth-child(1) { transform: rotate(0.8deg); }
    .spec:nth-child(2) { transform: rotate(-1.2deg); }
    .spec:nth-child(3) { transform: rotate(0.6deg); }
    .spec:hover { transform: rotate(0deg) scale(1.02); }
    .spec-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 2px solid var(--ink);
        flex-shrink: 0;
    }
    .spec:nth-child(1) .spec-dot { background: var(--red); }
    .spec:nth-child(2) .spec-dot { background: var(--yellow); }
    .spec:nth-child(3) .spec-dot { background: var(--blue); }
    .spec-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 600;
        color: var(--ink);
    }
    .spec-value {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.78rem;
        color: var(--ink);
        margin-top: 1px;
        letter-spacing: -0.01em;
    }

    /* ═══ SECCIÓN LABEL ═══ */
    .sec-label {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.15rem;
    }
    .sec-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background: var(--ink);
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .sec-label:nth-of-type(1) .sec-badge { background: var(--red); }
    .sec-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 700;
        color: var(--ink);
    }
    .sec-line {
        flex: 1;
        height: 3px;
        background: var(--ink);
    }

    /* ═══ CANVAS FRAME ═══ */
    .st-key-canvas_wrap {
        background: var(--surface);
        border: 3px solid var(--ink);
        padding: 1.2rem;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        position: relative;
        box-shadow: 10px 10px 0 var(--red);
        transition: box-shadow 0.2s ease;
    }
    .st-key-canvas_wrap:hover {
        box-shadow: 10px 10px 0 var(--blue);
    }
    .st-key-canvas_wrap::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        width: 20px;
        height: 20px;
        background: var(--yellow);
        border: 3px solid var(--ink);
        border-right: none;
        border-bottom: none;
    }
    .st-key-canvas_wrap::after {
        content: '';
        position: absolute;
        bottom: -3px;
        right: -3px;
        width: 20px;
        height: 20px;
        background: var(--yellow);
        border: 3px solid var(--ink);
        border-left: none;
        border-top: none;
    }
    .st-key-canvas_wrap [data-testid="stCanvas"] {
        margin: 0 auto;
        border-radius: 0;
        overflow: hidden;
    }
    .st-key-canvas_wrap canvas {
        border-radius: 0 !important;
        display: block;
    }

    /* ═══ INPUT API KEY ═══ */
    .stTextInput label,
    .stTextInput [data-testid="stWidgetLabel"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.74rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        color: var(--ink) !important;
    }
    .stTextInput div[data-baseweb="input"] > div,
    .stTextInput input {
        background: var(--surface) !important;
        border: 3px solid var(--ink) !important;
        border-radius: 0 !important;
        color: var(--ink) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        padding: 0.7rem 0.9rem !important;
        transition: all 0.15s ease !important;
    }
    .stTextInput div[data-baseweb="input"] > div:focus-within,
    .stTextInput input:focus {
        border-color: var(--blue) !important;
        box-shadow: 6px 6px 0 var(--yellow) !important;
        outline: none !important;
    }

    /* ═══ BOTÓN ═══ */
    .stButton > button {
        width: 100%;
        background: var(--red) !important;
        color: #ffffff !important;
        border: 3px solid var(--ink) !important;
        border-radius: 0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        padding: 0.9rem 1.4rem !important;
        box-shadow: 7px 7px 0 var(--ink) !important;
        transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button p {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover {
        background: var(--yellow) !important;
        color: var(--ink) !important;
        transform: translate(-2px, -2px);
        box-shadow: 9px 9px 0 var(--ink) !important;
    }
    .stButton > button:hover p { color: var(--ink) !important; }
    .stButton > button:active {
        transform: translate(3px, 3px);
        box-shadow: 4px 4px 0 var(--ink) !important;
    }

    /* ═══ RESULT FRAME ═══ */
    .result-frame {
        background: var(--surface);
        border: 3px solid var(--ink);
        padding: 1.6rem 1.75rem;
        margin-top: 1rem;
        position: relative;
        box-shadow: 10px 10px 0 var(--yellow);
    }
    .result-frame::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        height: 12px;
        background: repeating-linear-gradient(
            90deg,
            var(--red) 0 15px,
            var(--ink) 15px 30px,
            var(--yellow) 30px 45px,
            var(--ink) 45px 60px,
            var(--blue) 60px 75px,
            var(--ink) 75px 90px
        );
    }
    .result-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0 0.9rem 0;
        margin-bottom: 1.1rem;
        border-bottom: 2px solid var(--ink);
    }
    .result-head .title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--ink);
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
    }
    .result-head .title::before {
        content: '';
        width: 14px;
        height: 14px;
        background: var(--red);
        border: 2px solid var(--ink);
        border-radius: 50%;
        animation: pulse 1.8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50%      { transform: scale(0.7); opacity: 0.6; }
    }
    .result-head .meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
        background: var(--bg);
        padding: 0.3rem 0.65rem;
        border: 2px solid var(--ink);
    }

    /* Markdown del resultado */
    .result-frame .stMarkdown p,
    .result-frame .stMarkdown li {
        font-size: 1rem !important;
        line-height: 1.65 !important;
        color: var(--ink) !important;
    }

    /* LaTeX */
    .katex-display {
        background: #f7f2e5 !important;
        border: 2px solid var(--ink) !important;
        border-left: 8px solid var(--blue) !important;
        padding: 1rem 1.25rem !important;
        margin: 0.9rem 0 !important;
        overflow-x: auto !important;
        border-radius: 0 !important;
    }
    .katex { font-size: 1.15em !important; color: var(--ink) !important; }

    /* ═══ EMPTY STATE ═══ */
    .empty-frame {
        background: var(--surface);
        border: 3px dashed var(--ink);
        padding: 2.25rem 1.75rem;
        position: relative;
        text-align: center;
    }
    .empty-frame .shape {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        background: var(--yellow);
        border: 3px solid var(--ink);
        border-radius: 50%;
        font-size: 1.6rem;
        margin-bottom: 1rem;
    }
    .empty-frame .title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        color: var(--ink);
        line-height: 1.15;
        margin: 0 0 0.6rem 0;
    }
    .empty-frame .title .accent { color: var(--blue); }
    .empty-frame .text {
        font-size: 0.9rem;
        line-height: 1.55;
        color: var(--muted);
        margin: 0 auto;
        max-width: 340px;
    }

    /* ═══ TIPS AL PIE ═══ */
    .tips {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin-top: 3rem;
    }
    .tip {
        background: var(--surface);
        border: 3px solid var(--ink);
        padding: 1.25rem 1.35rem;
        position: relative;
        transition: all 0.2s ease;
    }
    .tip:nth-child(1) { box-shadow: 6px 6px 0 var(--red); }
    .tip:nth-child(2) { box-shadow: 6px 6px 0 var(--yellow); }
    .tip:nth-child(3) { box-shadow: 6px 6px 0 var(--blue); }
    .tip:hover {
        transform: translate(-3px, -3px);
    }
    .tip:nth-child(1):hover { box-shadow: 9px 9px 0 var(--red); }
    .tip:nth-child(2):hover { box-shadow: 9px 9px 0 var(--yellow); }
    .tip:nth-child(3):hover { box-shadow: 9px 9px 0 var(--blue); }

    .tip-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: var(--ink);
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        border-radius: 50%;
        margin-bottom: 0.7rem;
    }
    .tip:nth-child(1) .tip-num { background: var(--red); }
    .tip:nth-child(2) .tip-num { background: var(--yellow); color: var(--ink); }
    .tip:nth-child(3) .tip-num { background: var(--blue); }
    .tip-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        text-transform: uppercase;
        margin: 0 0 0.4rem 0;
        color: var(--ink);
    }
    .tip-text {
        font-size: 0.85rem;
        line-height: 1.55;
        color: var(--muted);
        margin: 0;
    }

    /* ═══ SPINNER ═══ */
    .stSpinner > div { border-top-color: var(--red) !important; }

    /* ═══ ALERTAS ═══ */
    [data-testid="stAlert"] {
        border-radius: 0 !important;
        border: 3px solid var(--ink) !important;
        border-left: 8px solid var(--red) !important;
        background: var(--surface) !important;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 12px; height: 12px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: var(--ink);
        border: 3px solid var(--bg);
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--red); }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 900px) {
        .hero { grid-template-columns: 60px 1fr; gap: 1rem; }
        .hero-shape { width: 60px; height: 90px; }
        .hero-shape .circle { width: 42px; height: 42px; }
        .hero-shape .square { width: 38px; height: 38px; top: 30px; left: 20px; }
        .hero-shape .triangle { border-left-width: 20px; border-right-width: 20px; border-bottom-width: 32px; }
        .hero-specs { grid-column: 1 / -1; flex-direction: row; flex-wrap: wrap; min-width: 0; }
        .spec { flex: 1 1 140px; }
        .hero h1 { font-size: 2.3rem !important; }
        .tips { grid-template-columns: 1fr; }
        .banner::before { width: 50px; }
        .banner-meta { display: none; }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return None


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div class="sb-head">
            <span class="eyebrow">◆ Control</span>
            <div class="title">Ajustes de trazo</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Grosor**")
    stroke_width = st.slider(
        "Grosor",
        1, 30, 5,
        label_visibility='collapsed',
    )

    st.markdown("---")
    st.caption(
        "**Consejo** · Dibuja con trazos claros y separados. "
        "Evita encimar líneas para mejor precisión."
    )


# ═══════════════════════════════════════════════════════════════
# BANNER SUPERIOR
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="banner">
        <div class="banner-left">
            <div class="banner-mark">◆</div>
            <div class="banner-title">Tablero Inteligente</div>
        </div>
        <div class="banner-meta">MODELO <b>GPT-4o MINI</b> · SALIDA ES</div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="hero">
        <div class="hero-shape">
            <div class="circle"></div>
            <div class="square"></div>
            <div class="triangle"></div>
        </div>
        <div class="hero-body">
            <span class="hero-eyebrow">Reconocimiento · Visión · IA</span>
            <h1>
                Dibuja <span class="blue">algo</span>.<br>
                La máquina lo <span class="red">interpreta</span>.
            </h1>
            <p>Un lienzo simple que <span class="underline">traduce tus trazos en significado</span>. Resuelve operaciones matemáticas paso a paso, identifica figuras geométricas y describe lo que dibujas en español.</p>
        </div>
        <div class="hero-specs">
            <div class="spec">
                <span class="spec-dot"></span>
                <div>
                    <div class="spec-label">Modelo</div>
                    <div class="spec-value">GPT-4o mini</div>
                </div>
            </div>
            <div class="spec">
                <span class="spec-dot"></span>
                <div>
                    <div class="spec-label">Modo</div>
                    <div class="spec-value">Visión + texto</div>
                </div>
            </div>
            <div class="spec">
                <span class="spec-dot"></span>
                <div>
                    <div class="spec-label">Salida</div>
                    <div class="spec-value">Español · LaTeX</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1.1, 1], gap="large")

# ─── Columna izquierda: canvas ───
with col_left:
    st.markdown("""
        <div class="sec-label">
            <span class="sec-badge">1</span>
            <span class="sec-text">Lienzo</span>
            <span class="sec-line"></span>
        </div>
    """, unsafe_allow_html=True)

    with st.container(key="canvas_wrap"):
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=300,
            width=400,
            drawing_mode="freedraw",
            key="canvas",
        )

# ─── Columna derecha: control + resultado ───
with col_right:
    st.markdown("""
        <div class="sec-label">
            <span class="sec-badge">2</span>
            <span class="sec-text">Análisis</span>
            <span class="sec-line"></span>
        </div>
    """, unsafe_allow_html=True)

    ke = st.text_input(
        "Clave de OpenAI",
        type="password",
        placeholder="sk-...",
    )
    os.environ['OPENAI_API_KEY'] = ke
    api_key = os.environ['OPENAI_API_KEY']

    if api_key:
        client = OpenAI(api_key=api_key)

    st.markdown("<div style='height: 0.85rem'></div>", unsafe_allow_html=True)

    analyze_button = st.button("▶ Analizar boceto", type="secondary")

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    result_slot = st.container()


# ═══════════════════════════════════════════════════════════════
# PROMPT
# ═══════════════════════════════════════════════════════════════
prompt_text = """Eres un tutor de matemáticas que analiza bocetos dibujados a mano.

IMPORTANTE: Responde SIEMPRE en español.

Paso 1 — Identifica: Determina si el boceto contiene un problema matemático, ecuación, fórmula o figura geométrica.

Paso 2 — Si SÍ contiene matemáticas:
- Escribe primero la operación tal como la interpretas, usando notación LaTeX entre signos de dólar, por ejemplo: $2x + 3 = 7$
- Luego resuelve paso a paso. Cada paso debe ir en su propia línea con LaTeX, así:
  $2x + 3 = 7$
  $2x = 7 - 3$
  $2x = 4$
  $x = 2$
- Al final escribe: **Respuesta final:** $x = 2$

Paso 3 — Si NO contiene matemáticas:
- Describe qué representa el boceto.
- Menciona las formas, símbolos u objetos que reconoces.

Sé claro y ordenado. Usa LaTeX para toda expresión matemática."""


# ═══════════════════════════════════════════════════════════════
# ANÁLISIS
# ═══════════════════════════════════════════════════════════════
if canvas_result.image_data is not None and api_key and analyze_button:

    with result_slot:
        with st.spinner("Analizando boceto..."):
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
            input_image.save('img.png')

            base64_image = encode_image_to_base64("img.png")

            if base64_image is None:
                st.error("No se pudo procesar la imagen del lienzo.")
            else:
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Eres un tutor de matemáticas. Responde SIEMPRE en español, "
                                    "sin excepción. Usa notación LaTeX entre signos $ para todas "
                                    "las expresiones matemáticas. Muestra cada paso de la solución "
                                    "en su propia línea."
                                ),
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_text},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_image}",
                                        },
                                    },
                                ],
                            },
                        ],
                        max_tokens=500,
                    )

                    content = response.choices[0].message.content or ""

                    st.markdown("""
                        <div class="result-frame">
                            <div class="result-head">
                                <span class="title">Resultado</span>
                                <span class="meta">GPT-4o mini</span>
                            </div>
                    """, unsafe_allow_html=True)

                    st.markdown(content, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.session_state.mi_respuesta = content

                except Exception as e:
                    st.error(f"Error: {e}")

elif not api_key and analyze_button:
    with result_slot:
        st.warning("⚠️ Ingresa tu API key de OpenAI para continuar.")

elif not analyze_button:
    with result_slot:
        st.markdown("""
            <div class="empty-frame">
                <div class="shape">◆</div>
                <p class="title">Sin boceto<br><span class="accent">por analizar</span></p>
                <p class="text">Dibuja en el lienzo, ingresa tu clave y presiona el botón. El resultado aparecerá aquí.</p>
            </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TIPS AL PIE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="tips">
        <div class="tip">
            <span class="tip-num">1</span>
            <h4 class="tip-title">Traza limpio</h4>
            <p class="tip-text">Líneas definidas y bien separadas. Evita encimar trazos que confundan al modelo.</p>
        </div>
        <div class="tip">
            <span class="tip-num">2</span>
            <h4 class="tip-title">Prueba matemáticas</h4>
            <p class="tip-text">Escribe 2+2, una ecuación como x²=9, o dibuja un triángulo, círculo o rectángulo.</p>
        </div>
        <div class="tip">
            <span class="tip-num">3</span>
            <h4 class="tip-title">Dibujo libre</h4>
            <p class="tip-text">Si dibujas algo diferente, la IA describirá qué ve: formas, objetos y su posible significado.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
