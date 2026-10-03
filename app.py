import os
import base64
import numpy as np
import streamlit as st
from PIL import Image
from openai import OpenAI
import openai
from streamlit_drawable_canvas import st_canvas

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title='Tablero Inteligente', page_icon='🧠')
st.title('Tablero Inteligente')

with st.sidebar:
    st.subheader("Acerca de:")
    st.write(
        "En esta aplicación veremos la capacidad que ahora tiene una máquina "
        "de interpretar un boceto dibujado a mano. Puede resolver operaciones "
        "matemáticas, identificar figuras geométricas o describir lo que veas."
    )

st.subheader("Dibuja el boceto en el panel y presiona el botón para analizarlo")


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
# CANVAS DE DIBUJO
# ═══════════════════════════════════════════════════════════════
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000"
bg_color = '#FFFFFF'

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)


# ═══════════════════════════════════════════════════════════════
# API KEY
# ═══════════════════════════════════════════════════════════════
ke = st.text_input('Ingresa tu Clave', type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

if api_key:
    client = OpenAI(api_key=api_key)


# ═══════════════════════════════════════════════════════════════
# BOTÓN DE ANÁLISIS
# ═══════════════════════════════════════════════════════════════
analyze_button = st.button("Analiza la imagen", type="secondary")


# ═══════════════════════════════════════════════════════════════
# PROMPT (en español + LaTeX)
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

    with st.spinner("Analizando..."):

        # Convertir canvas a imagen y guardarla
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')

        # Codificar en base64
        base64_image = encode_image_to_base64("img.png")

        if base64_image is None:
            st.error("No se pudo procesar la imagen del canvas.")
        else:
            try:
                full_response = ""
                message_placeholder = st.empty()

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

                if response.choices[0].message.content is not None:
                    full_response += response.choices[0].message.content
                    message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

                # Actualización final (sin cursor)
                message_placeholder.markdown(full_response, unsafe_allow_html=True)

                st.session_state.mi_respuesta = response.choices[0].message.content

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
