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
    page_icon='🧠',
    layout='wide',
    initial_sidebar_state='collapsed',
)

# ═══════════════════════════════════════════════════════════════
# ESTILOS — CREATIVE STUDIO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #f5f0e6;
        --paper: #ffffff;
        --ink: #14120e;
        --muted: #7a7468;
        --border: #e6dfd0;
        --accent: #ff5a36;
        --accent-soft: #fff0eb;
        --shadow: rgba(20, 18, 14, 0.10);
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        color: var(--ink);
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Instrument Serif', serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        color: var(--ink) !important;
    }

    /* ═══ FONDO ═══ */
    .stApp {
        background-color: var(--bg) !important;
        background-image:
            radial-gradient(circle at 10% -5%, rgba(255, 90, 54, 0.10), transparent 42%),
            radial-gradient(circle at 90% 105%, rgba(255, 209, 102, 0.14), transparent 45%),
            repeating-linear-gradient(
                45deg,
                transparent 0 22px,
                rgba(20, 18, 14, 0.012) 22px 24px
            );
        background-attachment: fixed;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1180px !important;
    }

    /* ═══ SIDEBAR ═══ */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--ink) !important; }

    .sb-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding-bottom: 1.1rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid var(--border);
    }
    .sb-brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #ff5a36, #ff8e53);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 6px 16px rgba(255, 90, 54, 0.32);
        flex-shrink: 0;
    }
    .sb-brand-text .name {
        font-family: 'Instrument Serif', serif;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1;
        color: var(--ink);
        letter-spacing: -0.01em;
    }
    .sb-brand-text .tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
        margin-top: 4px;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-size: 0.83rem !important;
        font-weight: 600 !important;
        color: #4c4740 !important;
    }

    /* Slider del sidebar */
    [data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(255, 90, 54, 0.16) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, var(--accent), #ff8e53) !important;
    }

    /* ═══ HERO ═══ */
    .hero {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 2rem;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border);
    }
    .hero-left { flex: 1; }
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        font-weight: 600;
        margin-bottom: 0.85rem;
    }
    .hero-kicker::before {
        content: '';
        display: inline-block;
        width: 22px;
        height: 2px;
        background: var(--accent);
    }
    .hero h1 {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.2rem !important;
        line-height: 1 !important;
        letter-spacing: -0.025em !important;
        font-weight: 600 !important;
        margin: 0 0 0.65rem 0 !important;
        color: var(--ink) !important;
    }
    .hero h1 em {
        font-style: italic;
        color: var(--accent);
        font-weight: 400;
    }
    .hero p {
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.55;
        margin: 0;
        max-width: 560px;
    }
    .hero-chips {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }
    .hero-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 100px;
        padding: 0.45rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--ink);
        white-space: nowrap;
    }
    .hero-chip .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
    }

    /* ═══ STEP LABEL (arriba de cada bloque) ═══ */
    .step-label {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--ink);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .step-label .num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 8px;
        background: var(--ink);
        color: #ffffff !important;
        font-size: 0.68rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    .step-label .line {
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* ═══ MARCO DEL CANVAS (polaroid) ═══ */
    .st-key-canvas_wrap {
        background: #ffffff;
        border: 2px solid var(--ink);
        border-radius: 20px;
        padding: 1.25rem;
        box-shadow: 12px 12px 0 var(--accent);
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    .st-key-canvas_wrap:hover {
        box-shadow: 16px 16px 0 var(--accent);
        transform: translateY(-3px);
    }
    .st-key-canvas_wrap [data-testid="stCanvas"] {
        margin: 0 auto;
        border-radius: 10px;
        overflow: hidden;
    }
    .st-key-canvas_wrap canvas {
        border-radius: 10px !important;
        display: block;
    }

    /* Etiqueta arriba del canvas */
    .canvas-label {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
        padding: 0 0.35rem 0.7rem 0.35rem;
    }
    .canvas-label .hint {
        color: var(--accent);
        font-weight: 600;
    }

    /* ═══ INPUT DE API KEY ═══ */
    .stTextInput label,
    .stTextInput [data-testid="stWidgetLabel"] p {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        color: var(--ink) !important;
        font-weight: 600 !important;
    }
    .stTextInput div[data-baseweb="input"] > div,
    .stTextInput input {
        background: #ffffff !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--ink) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stTextInput div[data-baseweb="input"] > div:focus-within,
    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(255, 90, 54, 0.14) !important;
        outline: none !important;
    }

    /* ═══ BOTÓN PRINCIPAL ═══ */
    .stButton > button {
        width: 100%;
        background: var(--ink) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.85rem 1.4rem !important;
        box-shadow: 6px 6px 0 var(--accent) !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .stButton > button p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    .stButton > button:hover {
        background: var(--accent) !important;
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0 var(--ink) !important;
    }
    .stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 4px 4px 0 var(--accent) !important;
    }

    /* ═══ TARJETA DE RESULTADO ═══ */
    .result-card {
        background: #ffffff;
        border: 2px solid var(--ink);
        border-radius: 20px;
        padding: 1.75rem 1.9rem;
        box-shadow: 10px 10px 0 var(--accent);
        margin-top: 1rem;
        position: relative;
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: -2px; left: -2px;
        width: 0; height: 0;
        border-top: 20px solid var(--accent);
        border-right: 20px solid transparent;
    }
    .result-head {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 1.2rem;
    }
    .result-head .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 12px var(--accent);
        animation: pulse-dot 1.8s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%      { opacity: 0.5; transform: scale(0.85); }
    }

    /* ═══ AJUSTES AL MARKDOWN DE LA RESPUESTA ═══ */
    .result-card .stMarkdown p,
    .result-card .stMarkdown li {
        font-size: 1rem !important;
        line-height: 1.65 !important;
        color: var(--ink) !important;
    }
    .result-card .stMarkdown h1,
    .result-card .stMarkdown h2,
    .result-card .stMarkdown h3 {
        margin-top: 1.2rem !important;
        margin-bottom: 0.6rem !important;
    }
    /* LaTeX display */
    .katex-display {
        background: #faf7f0 !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        margin: 0.85rem 0 !important;
        overflow-x: auto !important;
    }
    .katex { font-size: 1.15em !important; color: var(--ink) !important; }

    /* ═══ ESTADO VACÍO ═══ */
    .empty-state {
        background: #ffffff;
        border: 2px dashed var(--border);
        border-radius: 20px;
        padding: 2.5rem 1.75rem;
        text-align: center;
        margin-top: 1rem;
    }
    .empty-state .icon {
        font-size: 3rem;
        margin-bottom: 0.75rem;
        display: block;
        filter: grayscale(0.2);
    }
    .empty-state .title {
        font-family: 'Instrument Serif', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--ink);
        margin: 0 0 0.35rem 0;
    }
    .empty-state .text {
        font-size: 0.9rem;
        color: var(--muted);
        line-height: 1.55;
        margin: 0 auto;
        max-width: 340px;
    }

    /* ═══ TIPS AL PIE ═══ */
    .tips {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 3rem;
    }
    .tip {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        transition: all 0.2s ease;
    }
    .tip:hover {
        border-color: var(--accent);
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(255, 90, 54, 0.10);
    }
    .tip-icon {
        font-size: 1.4rem;
        margin-bottom: 0.55rem;
        display: block;
    }
    .tip-title {
        font-family: 'Instrument Serif', serif;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        color: var(--ink);
        letter-spacing: -0.01em;
    }
    .tip-text {
        font-size: 0.83rem;
        line-height: 1.5;
        color: var(--muted);
        margin: 0;
    }

    /* ═══ SPINNER ═══ */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* ═══ ALERTAS ═══ */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: #d8cebc;
        border-radius: 10px;
        border: 2px solid var(--bg);
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 900px) {
        .hero { flex-direction: column; align-items: flex-start; }
        .hero-chips { justify-content: flex-start; }
        .hero h1 { font-size: 2.3rem !important; }
        .tips { grid-template-columns: 1fr; }
        .st-key-canvas_wrap { box-shadow: 8px 8px 0 var(--accent); padding: 0.9rem; }
        .result-card { box-shadow: 6px 6px 0 var(--accent); padding: 1.35rem; }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════
def encode_image_to_base64(image_path):
    """Codifica una imagen a base64 para enviarla a la API."""
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
        <div class="sb-brand">
            <div class="sb-brand-mark">🧠</div>
            <div class="sb-brand-text">
                <div class="name">Tablero Inteligente</div>
                <div class="tag">Bocetos · IA · v1.0</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**✏️ Grosor del trazo**")
    stroke_width = st.slider(
        "Grosor del trazo",
        1, 30, 5,
        label_visibility='collapsed',
    )

    st.markdown("---")
    st.caption(
        "💡 **Consejo:** dibuja con trazos claros y bien definidos "
        "para obtener el mejor análisis posible."
    )


# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="hero">
        <div class="hero-left">
            <div class="hero-kicker">Bocetos interpretados con IA</div>
            <h1>Tablero <em>inteligente</em></h1>
            <p>Dibuja lo que quieras: una operación, una ecuación o una figura.
            Presiona <strong>Analizar</strong> y la IA te dirá qué ve y cómo resolverlo.</p>
        </div>
        <div class="hero-chips">
            <span class="hero-chip"><span class="dot"></span> GPT-4o mini</span>
            <span class="hero-chip"><span class="dot"></span> Reconoce matemáticas</span>
            <span class="hero-chip"><span class="dot"></span> En español</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# LAYOUT PRINCIPAL
# ═══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1.1, 1], gap="large")

# ─── Columna izquierda: canvas ───
with col_left:
    st.markdown("""
        <div class="step-label">
            <span class="num">1</span>
            <span>Dibuja tu boceto</span>
            <span class="line"></span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="canvas-label">
            <span>📐 Lienzo 400 × 300</span>
            <span class="hint">Trazo libre</span>
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

# ─── Columna derecha: API key + botón + resultado ───
with col_right:
    st.markdown("""
        <div class="step-label">
            <span class="num">2</span>
            <span>Configura y analiza</span>
            <span class="line"></span>
        </div>
    """, unsafe_allow_html=True)

    ke = st.text_input(
        "API key de OpenAI",
        type="password",
        placeholder="sk-...",
    )
    os.environ['OPENAI_API_KEY'] = ke
    api_key = os.environ['OPENAI_API_KEY']

    if api_key:
        client = OpenAI(api_key=api_key)

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    analyze_button = st.button("🔍  Analizar imagen", type="secondary")

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    # ─── Zona de resultado ───
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
        with st.spinner("Analizando tu boceto..."):
            # Convertir canvas a imagen y guardarla
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
            input_image.save('img.png')

            base64_image = encode_image_to_base64("img.png")

            if base64_image is None:
                st.error("No se pudo procesar la imagen del canvas.")
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

                    # Tarjeta de resultado con encabezado
                    st.markdown("""
                        <div class="result-card">
                            <div class="result-head">
                                <span class="dot"></span>
                                <span>Análisis del boceto</span>
                            </div>
                    """, unsafe_allow_html=True)

                    st.markdown(content, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.session_state.mi_respuesta = content

                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")

elif not api_key and analyze_button:
    with result_slot:
        st.warning("⚠️ Por favor ingresa tu API key de OpenAI para continuar.")

elif not analyze_button:
    with result_slot:
        st.markdown("""
            <div class="empty-state">
                <span class="icon">🎨</span>
                <p class="title">Esperando tu boceto</p>
                <p class="text">Dibuja algo en el lienzo, ingresa tu clave y presiona <strong>Analizar imagen</strong> para ver el resultado aquí.</p>
            </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TIPS AL PIE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="tips">
        <div class="tip">
            <span class="tip-icon">✏️</span>
            <h4 class="tip-title">Traza claro</h4>
            <p class="tip-text">Dibuja con líneas definidas y bien separadas. Evita trazos encimados que puedan confundir al modelo.</p>
        </div>
        <div class="tip">
            <span class="tip-icon">➗</span>
            <h4 class="tip-title">Prueba con matemáticas</h4>
            <p class="tip-text">Escribe una operación como 2+2, una ecuación como x²=9 o dibuja un triángulo, círculo o rectángulo.</p>
        </div>
        <div class="tip">
            <span class="tip-icon">💡</span>
            <h4 class="tip-title">Cosas no matemáticas</h4>
            <p class="tip-text">Si dibujas algo diferente, la IA describirá qué ve: formas, objetos, símbolos y lo que representan.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
