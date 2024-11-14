import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Función para convertir la imagen a base64
def image_to_base64(img):
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Configuración de la página
st.set_page_config(layout="wide", page_title="SantaElla", page_icon="<3")

# CSS para barra de navegación personalizada y fondo rosa claro
st.markdown("""
    <style>
          /* Barra de navegación */
        .css-1v3fvcr {
            background-color: #FF6F61;  /* Color de fondo de la barra lateral */
        }

        /* Texto de la barra de navegación */
        .css-1d391kg {
            color: white;  /* Color del texto en la barra lateral */
        }

        /* Fondo de la página principal */
        body {
            background-color: #f1d1d6;  /* Color de fondo de la página principal */
        }

        /* Estilo para el contenido de la página */
        body {
            background-color: #f1d1d6;  /* Rosa claro */
        }

        /* Personalizar otras secciones de la página */
        .titulo {
            text-align: center;
            font-size: 40px;
            color: #2a9d8f;
        }

        .subtitulo {
            text-align: center;
            font-size: 24px;
            color: #e76f51;
        }

        .descripcion {
            font-size: 18px;
            line-height: 1.6;
            margin-top: 20px;
        }

        .team-member {
            text-align: center;
            margin: 20px;
            padding: 10px;
            border-radius: 10px;
            background-color: #f1faee;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 16px;
        }

        .footer a {
            color: #e76f51;
            text-decoration: none;
            padding: 0 10px;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Cargar la imagen del logo
image = Image.open("./static/Santaellalogo.jpg")  # Ruta de la imagen

# Centrar el logo usando HTML y CSS en un bloque Markdown
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_to_base64(image)}" width="500"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Título y subtítulo
st.markdown('<h1 class="titulo">Proyecto Integrador: Santaella</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitulo">Santaella Oficial</h2>', unsafe_allow_html=True)

# Descripción del proyecto
st.markdown('<div class="descripcion">', unsafe_allow_html=True)
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
""")  # Este es tu texto original

st.markdown('</div>', unsafe_allow_html=True)

# Sección de integrantes del equipo
st.header("Nuestro Equipo")
col1, col2, col3 = st.columns(3)

# Integrantes con diseño tipo tarjeta
with col1:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("./static/Lina.jpeg", width=200)
    st.write("**Lina Patricia Cadavid**")
    st.write("Estudiante Nuevas Tecnologías")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("./static/Carol.jpeg", width=200)
    st.write("**Carol Eliana Gonzalez**")
    st.write("Estudiante Nuevas Tecnologías")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("./static/Jose.jpeg", width=200)
    st.write("**José Castro Molina**")
    st.write("Estudiante Nuevas Tecnologías")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("./static/Roi.jpeg", width=200)
    st.write("**Roicer Romero**")
    st.write("Estudiante Nuevas Tecnologías")
    st.markdown('</div>', unsafe_allow_html=True)

with col1:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("./static/Jero.jpeg", width=200)
    st.write("**Jeronimo**")
    st.write("Estudiante Nuevas Tecnologías")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer con enlaces
st.markdown(
    """
    <div class="footer">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
