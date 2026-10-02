import os
from openai import OpenAI
import streamlit as st

# Configuración de la interfaz web
st.set_page_config(
    page_title="Asistente IA", page_icon="🤖", layout="centered"
)
st.title("🤖 Asistente Inteligente")
st.caption(
    "Hazme cualquier pregunta basada en la información cargada en el sistema."
)

# ==============================================================================
# 1. AQUÍ PEGAS TU API KEY DE OPENROUTER
# ==============================================================================
# Reemplaza el texto entre comillas con tu clave real de OpenRouter (empieza con "sk-or-v1-..."):
OPENROUTER_API_KEY = os.environ.get(
    "OPENROUTER_API_KEY",
    "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",  # <-- PEGA TU CLAVE AQUÍ
)

MODELO = "openrouter/free"

# Conexión al cliente de OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ==============================================================================
# 2. ENLACE CON TU ARCHIVO DE INSTRUCCIONES / INFORMACIÓN
# ==============================================================================
ARCHIVO_DATOS = "instrucciones.txt"


def leer_instrucciones():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Eres un asistente servicial y respondes basándote en la información dada."


INSTRUCCIONES_SISTEMA = leer_instrucciones()

# ==============================================================================
# 3. MEMORIA DEL CHAT
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================================================================
# 4. CHAT EN VIVO Y RESPUESTA DE LA IA
# ==============================================================================
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    # 1. Mostrar y guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta con OpenRouter
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Preparamos el contexto enviando tus instrucciones y el historial
                mensajes_a_enviar = [
                    {"role": "system", "content": INSTRUCCIONES_SISTEMA}
                ] + st.session_state.messages

                response = client.chat.completions.create(
                    model=MODELO,
                    messages=mensajes_a_enviar,
                )

                respuesta_texto = response.choices[0].message.content
                st.markdown(respuesta_texto)

                # Guardar respuesta del bot en la memoria
                st.session_state.messages.append(
                    {"role": "assistant", "content": respuesta_texto}
                )
            except Exception as e:
                st.error(f"Error al conectar con OpenRouter: {e}")
