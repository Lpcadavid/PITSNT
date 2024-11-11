import streamlit as st
import google.generativeai as genai

# Configura la API Key de Google Generative AI
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Crea la interfaz de usuario con Streamlit
st.title("Generador de Texto con Gemini 1.5")

# Subir archivo o ingresar texto manualmente
uploaded_file = st.file_uploader("Sube un archivo de texto", type=["txt"])
user_input = st.text_input("O ingresa tu texto aquí:")

# Lee el contenido del archivo si está cargado
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.write("Contenido del archivo cargado:")
    st.write(content)
else:
    content = user_input

# Genera la respuesta a preguntas sobre el contenido
question = st.text_input("Haz una pregunta sobre el contenido:")
if st.button("Generar respuesta"):
    if content and question:
        # Combina el contenido con la pregunta
        prompt = f"{content}\n\nPregunta: {question}"
        response = model.generate_content(prompt)
        st.write("Respuesta:", response.text)
    else:
        st.write("Por favor sube un archivo o ingresa un texto y haz una pregunta.")
