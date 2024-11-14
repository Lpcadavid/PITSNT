import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Función para convertir la imagen a base64
def image_to_base64(img):
    # Convertir la imagen a RGB en caso de que tenga un canal alfa
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # Guardar como JPEG
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Configuración de la página
st.set_page_config(layout="wide", page_title="SantaElla", page_icon="<3")

# Cargar la imagen del logo
image = Image.open("./static/Santaellalogo.jpg")  # Ruta de la imagen

# Centrar el logo usando HTML y CSS en un bloque Markdown
st.markdown(
    """
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{}" width="500"/>
    </div>
    """.format(image_to_base64(image)),
    unsafe_allow_html=True
)

# Título y subtítulo
st.title("Proyecto Integrador: Inventario Santaella")
st.subheader("Santaella Oficial")

# Integrantes
st.header("Nuestro Equipo")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("./static/Lina.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Lina Patricia Cadavid**")
    st.write("Estudiante Nuevas Tecnologías")

with col2:
    st.image("./static/Carol.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Carol Eliana Gonzalez**")
    st.write("Estudiante Nuevas Tecnologías")

with col3:
    st.image("./static/Jose.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**José Castro Molina**")
    st.write("Estudiante Nuevas Tecnológias")

with col2:
    st.image("./static/Roi.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Roicer Romero**")
    st.write("Estudiante Nuevas Tecnológias")

with col1:
    st.image("./static/Jero.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Jeronimo**")
    st.write("Estudiante Nuevas Tecnológias")

# Descripción del proyecto con títulos en negrita
st.header("Sobre SantaElla")

st.write("""
**Objetivo Principal**: Crear una plataforma en línea elegante y funcional para la venta de bisutería femenina, 
         que incluya un sistema de inventario básico para gestionar de manera eficiente los productos y asegurar 
         una experiencia de compra fluida y encantadora para nuestras clientas.

**Problemática**: En el competitivo mundo de la moda y los accesorios, muchas pequeñas empresas de 
         bisutería enfrentan desafíos significativos en la gestión de su inventario. La falta de un sistema organizado 
         puede llevar a problemas como el desabastecimiento, el exceso de stock y la dificultad para realizar un seguimiento
          preciso de las ventas y los productos disponibles. Esto no solo afecta la eficiencia operativa, sino que también puede 
         resultar en una experiencia de cliente insatisfactoria.

**Enfoque**: Nuestro proyecto, “Santaella”, aborda esta problemática mediante el desarrollo de una página web intuitiva 
         y atractiva que no solo exhibe nuestra exquisita colección de bisutería, sino que también integra un sistema de 
         inventario básico. Este sistema permitirá:

**Gestión de Stock en Tiempo Real**: Actualizaciones automáticas del inventario con cada venta, asegurando que siempre se muestre la
          disponibilidad actual de los productos.

**Alertas de Reabastecimiento**: Notificaciones cuando los niveles de stock caen por debajo de un umbral predefinido, ayudando a evitar 
         desabastecimientos.

**Historial de Ventas**: Registro detallado de todas las transacciones, facilitando el análisis de tendencias de ventas y la planificación
          de inventario.

**Interfaz Amigable**: Un diseño intuitivo que permite a los administradores gestionar el inventario sin necesidad de conocimientos 
         técnicos avanzados.

Con “Santaella”, no solo buscamos embellecer a nuestras clientas con piezas únicas y deslumbrantes, sino también empoderar a 
         nuestra empresa con herramientas que optimicen la gestión y potencien el crecimiento. ¡Porque cada detalle cuenta 
         cuando se trata de brillar!
""")

# Footer con links
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
