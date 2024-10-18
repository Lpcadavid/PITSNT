import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  

st.set_page_config(layout="wide")

st.subheader("Proyecto Integrador")

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:  
    # Cargar las credenciales de Firebase desde los secretos de Streamlit
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]  
    # Convertir las credenciales a un diccionario Python
    secrets_dict = firebase_credentials.to_dict()  
    # Crear un objeto de credenciales usando el diccionario 
    cred = credentials.Certificate(secrets_dict)  
    # Inicializar la aplicación de Firebase con las credenciales
    app = firebase_admin.initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''   

    ### Introducción

    -   El proyecto consiste en el desarrollo de una base de datos en Python para gestionar los productos, clientes y ventas de una pequeña empresa de accesorios. Esta base de datos permitirá llevar un control más eficiente y organizado de la información.
    -   El objetivo principal es crear una herramienta que facilite la gestión de inventario y relaciones con los clientes, mejorando la toma de decisiones y optimizando procesos.
    -   Una buena gestión de datos es crucial para cualquier negocio. Permite identificar tendencias, gestionar el stock de manera efectiva y mejorar el servicio al cliente, lo que puede resultar en un aumento de las ventas y satisfacción del cliente.
                

    ### Desarrollo

    -   La base de datos se diseñará para almacenar información sobre productos (nombre, categoría, precio, stock), clientes (nombre, contacto, historial de compras) y ventas (fecha, productos vendidos, monto total). Utilizaré Python con una biblioteca como SQLite para crear y manejar la base de datos.
    -   Análisis de requisitos: Definir qué información es esencial para el negocio.
        Diseño de la base de datos: Estructurar las tablas y relaciones entre ellas.
        Implementación: Programar la base de datos en Python utilizando SQLite. Incluirá funcionalidades como agregar, editar y eliminar productos, así como registrar ventas y consultar datos.
        Pruebas: Verificar que todas las funciones trabajen correctamente y que los datos se almacenen y recuperen adecuadamente.
                
    -   Se espera obtener una base de datos funcional que permita realizar un seguimiento en tiempo real del inventario y las ventas. Además, se generarán informes que ayuden a identificar qué productos son más populares y cuáles necesitan ser reabastecidos.

    ### Conclusión

    -   Resumen de los resultados
        Se logró desarrollar una base de datos que organiza de manera efectiva la información de la empresa. Esto permitirá una gestión más ágil y accesible de los datos.
    -   Logros alcanzados
        Implementación exitosa de la base de datos.
        Capacitación en el uso de Python y SQLite.
        Desarrollo de un sistema que facilita el seguimiento de ventas y clientes.
    -   Dificultades encontradas
        Desafíos en la estructuración inicial de la base de datos.
        Problemas de compatibilidad con diferentes versiones de bibliotecas.
        Aprendizaje de nuevas tecnologías que inicialmente resultaron complejas.
    -   Aportes personales
        Este proyecto me ha permitido mejorar mis habilidades en programación y gestión de bases de datos. También he aprendido sobre la importancia de la organización y la planificación en el desarrollo de un sistema que responda a las necesidades reales de un negocio.
    ''')

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tab_Generador:
    st.write('Esta función Python genera datos ficticios de usuarios y productos y los carga en una base de datos Firestore, proporcionando una interfaz sencilla para controlar la cantidad de datos generados y visualizar los resultados.')
    # Inicializar Faker para Colombia
    fake = Faker('es_CO')

    # Lista de ciudades colombianas
    ciudades_colombianas = [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 
        'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibagué',
        'Pasto', 'Manizales', 'Neiva', 'Villavicencio', 'Armenia'
    ]

    def generate_fake_users(n):
        users = []
        for _ in range(n):
            user = {
                'name': fake.name(),
                'email': fake.email(),
                'edad': random.randint(18, 80),
                'ciudad': random.choice(ciudades_colombianas)
            }
            users.append(user)
        return users

    def generate_fake_products(n):
        categories = {
            'Electrónica': [
                'Celular', 'Portátil', 'Tablet', 'Audífonos', 'Reloj inteligente', 
                'Cámara digital', 'Parlante Bluetooth', 'Batería portátil', 
                'Monitor', 'Teclado inalámbrico'
            ],
            'Ropa': [
                'Camiseta', 'Jean', 'Vestido', 'Chaqueta', 'Zapatos', 
                'Sudadera', 'Medias', 'Ruana', 'Gorra', 'Falda'
            ],
            'Hogar': [
                'Lámpara', 'Cojín', 'Cortinas', 'Olla', 'Juego de sábanas', 
                'Toallas', 'Espejo', 'Reloj de pared', 'Tapete', 'Florero'
            ],
            'Deportes': [
                'Balón de fútbol', 'Raqueta de tenis', 'Pesas', 
                'Colchoneta de yoga', 'Bicicleta', 'Tenis para correr', 
                'Maletín deportivo', 'Termo', 'Guantes de boxeo', 'Lazo para saltar'
            ]
        }

        products = []
        for _ in range(n):
            category = random.choice(list(categories.keys()))
            product_type = random.choice(categories[category])
            
            product = {
                'nombre': product_type,
                'precio': round(random.uniform(10000, 1000000), -3),  # Precios en pesos colombianos
                'categoria': category,
                'stock': random.randint(0, 100)
            }
            products.append(product)
        return products

    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('clientes')
        num_users = st.number_input('Número de clientes a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Clientes'):
            with st.spinner('Eliminando clientes existentes...'):
                delete_collection('clientes')
            with st.spinner('Generando y añadiendo nuevos clientes...'):
                users = generate_fake_users(num_users)
                add_data_to_firestore('clientes', users)
            st.success(f'{num_users} clientes añadidos a Firestore')
            st.dataframe(pd.DataFrame(users))

    with col2:
        st.subheader('Productos')
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Productos'):
            with st.spinner('Eliminando productos existentes...'):
                delete_collection('productos')
            with st.spinner('Generando y añadiendo nuevos productos...'):
                products = generate_fake_products(num_products)
                add_data_to_firestore('productos', products)
            st.success(f'{num_products} productos añadidos a Firestore')
            st.dataframe(pd.DataFrame(products))

#----------------------------------------------------------
#Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Esta función muestra datos de usuarios y productos almacenados en una base de datos Firestore, permitiendo una visualización organizada y fácil acceso a la información.')
    tab_user, tab_prodcutos = st.tabs(["Usuarios", "Prodcutos"])
    with tab_user:        
        # Obtener datos de una colección de Firestore
        users = db.collection('clientes').stream()
        # Convertir datos a una lista de diccionarios
        users_data = [doc.to_dict() for doc in users]
        # Crear DataFrame
        df_users = pd.DataFrame(users_data)
        # Reordenar las columnas
        column_order = ['name', 'email', 'edad', 'ciudad']
        df_users = df_users.reindex(columns=column_order)   

        st.dataframe(df_users)
    with tab_prodcutos:       
        # Obtener datos de una colección de Firestore
        users = db.collection('productos').stream()
        # Convertir datos a una lista de diccionarios
        users_data = [doc.to_dict() for doc in users]
        # Crear DataFrame
        df_products = pd.DataFrame(users_data)
         # Reordenar las columnas
        column_order = ['nombre', 'categoria', 'precio', 'stock']
        df_products = df_products.reindex(columns=column_order)
        
        st.dataframe(df_products)

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame.  **(df.head())**                              
    * Muestra la cantidad de filas y columnas del DataFrame.  **(df.shape)**
    * Muestra los tipos de datos de cada columna.  **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas.  **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())** 
    * Otra información importante  
    """)

    st.write("Primeras 5 filas de la tabla clientes")
    st.dataframe(df_users.head())

    st.write("Primeras 5 filas de la tabla Productos")
    st.dataframe(df_products.head())

    st.write("Cantidad de filas y columnas del Clientes")
    st.write(df_users.shape)

    st.write("Cantidad de filas y columnas del Productos")
    st.write(df_products.shape)

    # Mostrar los tipos de datos de cada columna
    st.write("**Tipos de datos Tabla Clientes:**")
    st.write(df_users.dtypes)

    st.write("**Tipos de datos Tabla Productos:**")
    st.write(df_products.dtypes)

    # Identificar y mostrar las columnas con valores nulos
    st.write("**Valores nulos por columna:**")
    st.write(df_users.isnull().sum())

    st.write("**Valores nulos por columna:**")
    st.write(df_products.isnull().sum())

    # Mostrar un resumen estadístico de las columnas numéricas
    st.write("**Resumen estadístico Clientes:**")
    st.write(df_users.describe())

    st.write("**Resumen estadístico Productos:**")
    st.write(df_products.describe())

    # Crear una lista de las columnas categóricas
    columnas_categoricas = df_users.select_dtypes(include=['object']).columns.tolist()
    columnas_categoricas = df_products.select_dtypes(include=['object']).columns.tolist()

 

    
#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtrado_Básico:
        st.title("Filtro Básico")
        st.markdown("""
        * Permite filtrar datos usando condiciones simples. **(df[df['columna'] == 'valor'])**
        * Permite seleccionar una columna y un valor para el filtro. **(st.selectbox, st.text_input)**
        * Permite elegir un operador de comparación (igual, diferente, mayor que, menor que). **(st.radio)**
        * Muestra los datos filtrados en una tabla. **(st.dataframe)** 
        """)


#----------------------------------------------------------
#Analítica 3
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)


