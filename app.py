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
    page_icon='◼',
    layout='wide',
    initial_sidebar_state='collapsed',
)

# ═══════════════════════════════════════════════════════════════
# ESTILOS — SWISS / INTERNATIONAL TYPOGRAPHIC
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --bg:        #fafafa;
        --surface:   #ffffff;
        --ink:       #0a0a0a;
        --ink-2:     #2a2a2a;
        --muted:     #757575;
        --line:      #d4d4d4;
        --line-hard: #0a0a0a;
        --red:       #e63329;
        --red-soft:  #fde8e6;
    }

    /* ═══ BASE ═══ */
    html, body, [class*="css"], .stApp, button, input, textarea, select {
        font-family: 'Inter Tight', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: var(--ink) !important;
        font-feature-settings: 'ss01', 'cv01';
    }
    h1, h2, h3, h4, h5 {
        font-family: 'Inter Tight', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em !important;
        color: var(--ink) !important;
    }

    .stApp {
        background-color: var(--bg) !important;
        background-image:
            linear-gradient(90deg, transparent 0 calc(50% - 0.5px), rgba(10, 10, 10, 0.025) calc(50% - 0.5px) calc(50% + 0.5px), transparent calc(50% + 0.5px));
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
        border-right: 1px solid var(--line-hard) !important;
    }
    [data-testid="stSidebar"] * { color: var(--ink) !important; }

    .sb-head {
        padding-bottom: 1rem;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid var(--ink);
    }
    .sb-head .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        color: var(--red);
        font-weight: 700;
        display: block;
        margin-bottom: 0.35rem;
    }
    .sb-head .title {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 800;
        font-size: 1.15rem;
        letter-spacing: -0.03em;
        line-height: 1;
        color: var(--ink);
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        color: var(--ink-2) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--ink) !important;
        border-color: var(--ink) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        width: 14px !important;
        height: 14px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
        background: var(--ink) !important;
        border-radius: 0 !important;
    }

    /* ═══ TOP BAR ═══ */
    .topbar {
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--ink);
        margin-bottom: 2.5rem;
    }
    .topbar-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        background: var(--ink);
        color: #ffffff;
        font-family: 'Inter Tight', sans-serif;
        font-weight: 900;
        font-size: 0.95rem;
        letter-spacing: -0.02em;
    }
    .topbar-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--ink);
        font-weight: 600;
    }
    .topbar-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 500;
        text-align: right;
    }
    .topbar-meta .sep {
        color: var(--red);
        margin: 0 0.4rem;
        font-weight: 700;
    }

    /* ═══ HERO ═══ */
    .hero-grid {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 2rem;
        align-items: end;
        padding-bottom: 2rem;
        margin-bottom: 2.5rem;
        border-bottom: 1px solid var(--line);
    }
    .hero-num {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 900;
        font-size: 5.5rem;
        line-height: 0.85;
        letter-spacing: -0.05em;
        color: var(--ink);
        font-feature-settings: 'tnum';
    }
    .hero-num .dot {
        color: var(--red);
    }
    .hero-body { padding-bottom: 0.35rem; }
    .hero-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--red);
        font-weight: 700;
        margin-bottom: 0.75rem;
        display: block;
    }
    .hero h1 {
        font-family: 'Inter Tight', sans-serif !important;
        font-size: 3.6rem !important;
        line-height: 0.95 !important;
        letter-spacing: -0.045em !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        margin: 0 0 1rem 0 !important;
        color: var(--ink) !important;
    }
    .hero h1 .stroke {
        -webkit-text-stroke: 2px var(--ink);
        color: transparent !important;
    }
    .hero p {
        font-size: 1rem;
        line-height: 1.55;
        color: var(--ink-2);
        margin: 0;
        max-width: 520px;
        font-weight: 400;
    }
    .hero-pillars {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
        text-align: right;
        padding-bottom: 0.35rem;
    }
    .pillar {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--ink-2);
        font-weight: 500;
        padding: 0.35rem 0.7rem;
        background: var(--surface);
        border: 1px solid var(--line);
    }
    .pillar.live {
        border-color: var(--red);
        color: var(--red);
        font-weight: 700;
    }
    .pillar.live::before {
        content: '● ';
        color: var(--red);
        animation: blink 1.6s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.3; }
    }

    /* ═══ SECTION LABEL ═══ */
    .sec-label {
        display: flex;
        align-items: baseline;
        gap: 0.9rem;
        margin-bottom: 1.25rem;
        padding-bottom: 0.65rem;
        border-bottom: 1px solid var(--line-hard);
    }
    .sec-num {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 900;
        font-size: 1.6rem;
        line-height: 1;
        color: var(--ink);
        letter-spacing: -0.04em;
    }
    .sec-num .accent { color: var(--red); }
    .sec-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--ink);
        font-weight: 600;
        flex: 1;
    }
    .sec-hint {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 500;
    }

    /* ═══ CANVAS FRAME ═══ */
    .st-key-canvas_wrap {
        background: var(--surface);
        border: 2px solid var(--ink);
        padding: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        position: relative;
    }
    .st-key-canvas_wrap::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(
            90deg,
            var(--red) 0 25%,
            var(--ink) 25% 50%,
            var(--ink) 50% 75%,
            var(--ink) 75% 100%
        );
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

    /* ═══ CORNER MARKS (sobre el canvas) ═══ */
    .canvas-corner {
        position: absolute;
        width: 12px;
        height: 12px;
        border: 2px solid var(--red);
        z-index: 10;
    }
    .canvas-corner.tl { top: 6px; left: 6px; border-right: none; border-bottom: none; }
    .canvas-corner.tr { top: 6px; right: 6px; border-left: none; border-bottom: none; }
    .canvas-corner.bl { bottom: 6px; left: 6px; border-right: none; border-top: none; }
    .canvas-corner.br { bottom: 6px; right: 6px; border-left: none; border-top: none; }

    /* ═══ INPUT API KEY ═══ */
    .stTextInput label,
    .stTextInput [data-testid="stWidgetLabel"] p {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        color: var(--ink) !important;
    }
    .stTextInput div[data-baseweb="input"] > div,
    .stTextInput input {
        background: var(--surface) !important;
        border: 1px solid var(--line-hard) !important;
        border-radius: 0 !important;
        color: var(--ink) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        padding: 0.7rem 0.9rem !important;
        transition: border-color 0.1s ease, background 0.1s ease !important;
    }
    .stTextInput div[data-baseweb="input"] > div:focus-within,
    .stTextInput input:focus {
        border-color: var(--red) !important;
        box-shadow: inset 4px 0 0 var(--red) !important;
        outline: none !important;
        background: var(--surface) !important;
    }

    /* ═══ BOTÓN PRINCIPAL ═══ */
    .stButton > button {
        width: 100%;
        background: var(--ink) !important;
        color: #ffffff !important;
        border: 2px solid var(--ink) !important;
        border-radius: 0 !important;
        font-family: 'Inter Tight', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        padding: 0.95rem 1.4rem !important;
        transition: all 0.12s ease !important;
    }
    .stButton > button p {
        color: #ffffff !important;
        font-family: 'Inter Tight', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover {
        background: var(--red) !important;
        border-color: var(--red) !important;
        color: #ffffff !important;
    }
    .stButton > button:hover p { color: #ffffff !important; }

    /* ═══ RESULT CARD ═══ */
    .result-frame {
        background: var(--surface);
        border: 2px solid var(--ink);
        padding: 1.75rem 1.9rem;
        position: relative;
    }
    .result-frame::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--red);
    }
    .result-head {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding-bottom: 0.85rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid var(--line);
    }
    .result-head .title {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 800;
        font-size: 0.95rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--ink);
    }
    .result-head .meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
    }

    /* LaTeX */
    .katex-display {
        background: #f5f5f5 !important;
        border-left: 4px solid var(--ink) !important;
        padding: 1rem 1.25rem !important;
        margin: 0.85rem 0 !important;
        overflow-x: auto !important;
    }
    .katex {
        font-size: 1.15em !important;
        color: var(--ink) !important;
    }

    /* Markdown dentro del resultado */
    .result-frame .stMarkdown p,
    .result-frame .stMarkdown li {
        font-size: 1rem !important;
        line-height: 1.65 !important;
        color: var(--ink) !important;
    }

    /* ═══ EMPTY STATE ═══ */
    .empty-frame {
        background: var(--surface);
        border: 1px solid var(--line);
        border-left: 4px solid var(--ink);
        padding: 2rem 1.85rem;
    }
    .empty-frame .tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.9rem;
        display: block;
    }
    .empty-frame .title {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 800;
        font-size: 1.4rem;
        letter-spacing: -0.03em;
        color: var(--ink);
        line-height: 1.15;
        margin: 0 0 0.65rem 0;
        text-transform: uppercase;
    }
    .empty-frame .title .accent { color: var(--red); }
    .empty-frame .text {
        font-size: 0.92rem;
        line-height: 1.6;
        color: var(--ink-2);
        margin: 0;
        max-width: 360px;
    }

    /* ═══ BOTTOM STRIP (info) ═══ */
    .bottom-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0;
        border-top: 2px solid var(--ink);
        margin-top: 3rem;
    }
    .strip-item {
        padding: 1.25rem 1.25rem 1.25rem 0;
        border-right: 1px solid var(--line);
    }
    .strip-item:last-child {
        border-right: none;
        padding-right: 0;
        padding-left: 1.25rem;
    }
    .strip-item:not(:first-child) {
        padding-left: 1.25rem;
    }
    .strip-item .idx {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--red);
        font-weight: 700;
        display: block;
        margin-bottom: 0.55rem;
    }
    .strip-item .head {
        font-family: 'Inter Tight', sans-serif;
        font-weight: 800;
        font-size: 1rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        color: var(--ink);
        margin: 0 0 0.35rem 0;
        line-height: 1.15;
    }
    .strip-item .body {
        font-size: 0.85rem;
        line-height: 1.5;
        color: var(--muted);
        margin: 0;
    }

    /* ═══ SPINNER ═══ */
    .stSpinner > div { border-top-color: var(--red) !important; }

    /* ═══ ALERTAS ═══ */
    [data-testid="stAlert"] {
        border-radius: 0 !important;
        border: 1px solid var(--ink) !important;
        border-left: 4px solid var(--red) !important;
        background: var(--surface) !important;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: var(--ink);
        border-radius: 0;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--red); }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 900px) {
        .hero-grid { grid-template-columns: 1fr; gap: 1.25rem; }
        .hero-pillars { text-align: left; }
        .hero h1 { font-size: 2.4rem !important; }
        .hero-num { font-size: 3.5rem; }
        .topbar { grid-template-columns: auto 1fr; }
        .topbar-meta { grid-column: 1 / -1; text-align: left; margin-top: 0.5rem; }
        .bottom-strip { grid-template-columns: 1fr; }
        .strip-item { border-right: none !important; border-bottom: 1px solid var(--line); padding: 1.1rem 0 !important; }
        .strip-item:last-child { border-bottom: none; }
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
            <span class="eyebrow">§ Panel</span>
            <div class="title">Herramientas</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Grosor del trazo**")
    stroke_width = st.slider(
        "Grosor del trazo",
        1, 30, 5,
        label_visibility='collapsed',
    )

    st.markdown("---")
    st.caption(
        "**Nota** · Dibuja con trazos claros y separados para "
        "mejorar la precisión del análisis."
    )


# ═══════════════════════════════════════════════════════════════
# TOP BAR
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="topbar">
        <div class="topbar-mark">T</div>
        <div class="topbar-title">Tablero Inteligente</div>
        <div class="topbar-meta">
            IA <span class="sep">/</span>
            Visión <span class="sep">/</span>
            Bocetos
        </div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="hero-grid">
        <div class="hero-num">01<span class="dot">.</span></div>
        <div class="hero-body">
            <span class="hero-eyebrow">Reconocimiento de bocetos</span>
            <h1>Dibuja.<br><span class="stroke">La máquina</span><br>interpreta.</h1>
            <p>Un lienzo simple que interpreta lo que dibujas. Resuelve operaciones, reconoce figuras y describe lo que ve — todo desde tu propio trazo.</p>
        </div>
        <div class="hero-pillars">
            <span class="pillar live">Modelo activo</span>
            <span class="pillar">GPT-4o mini</span>
            <span class="pillar">Salida en ES</span>
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
            <span class="sec-num">1<span class="accent">.</span></span>
            <span class="sec-title">Lienzo</span>
            <span class="sec-hint">400 × 300</span>
        </div>
    """, unsafe_allow_html=True)

    with st.container(key="canvas_wrap"):
        # Marcas de esquina
        st.markdown("""
            <div class="canvas-corner tl"></div>
            <div class="canvas-corner tr"></div>
            <div class="canvas-corner bl"></div>
            <div class="canvas-corner br"></div>
        """, unsafe_allow_html=True)

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
            <span class="sec-num">2<span class="accent">.</span></span>
            <span class="sec-title">Análisis</span>
            <span class="sec-hint">API Key</span>
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

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    analyze_button = st.button("Analizar boceto →", type="secondary")

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
                <span class="tag">— Esperando</span>
                <p class="title">Sin boceto<br>por <span class="accent">analizar</span></p>
                <p class="text">Dibuja en el lienzo, ingresa tu clave y presiona el botón para ver aquí el resultado.</p>
            </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# BOTTOM STRIP
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="bottom-strip">
        <div class="strip-item">
            <span class="idx">01 — Trazo</span>
            <p class="head">Líneas limpias</p>
            <p class="body">Dibuja con trazos definidos y bien separados. Evita encimar líneas que puedan confundir al modelo.</p>
        </div>
        <div class="strip-item">
            <span class="idx">02 — Matemáticas</span>
            <p class="head">Operaciones y figuras</p>
            <p class="body">Escribe una operación como 2+2, una ecuación como x²=9, o dibuja triángulos, círculos y rectángulos.</p>
        </div>
        <div class="strip-item">
            <span class="idx">03 — Libre</span>
            <p class="head">Cualquier cosa</p>
            <p class="body">Si dibujas algo distinto, la IA describirá qué ve: formas, objetos, símbolos y su posible significado.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
