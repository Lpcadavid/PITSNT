import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  
import matplotlib.pyplot as plt
import seaborn as sns


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


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtro Final Dinámico"])


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
# Análisis Exploratorio
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame. **(df.head())**
    * Muestra la cantidad de filas y columnas del DataFrame. **(df.shape)**
    * Muestra los tipos de datos de cada columna. **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas. **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())** 
    * Otra información importante
    """)

    # Mostrar las primeras filas
    st.write("Primeras 5 filas de la tabla clientes")
    st.dataframe(df_users.head())

    st.write("Primeras 5 filas de la tabla Productos")
    st.dataframe(df_products.head())

    # Estadísticas y análisis básico
    st.write("Cantidad de filas y columnas del Clientes")
    st.write(df_users.shape)

    st.write("Cantidad de filas y columnas del Productos")
    st.write(df_products.shape)

    st.write("**Tipos de datos Tabla Clientes:**")
    st.write(df_users.dtypes)

    st.write("**Tipos de datos Tabla Productos:**")
    st.write(df_products.dtypes)

    st.write("**Valores nulos por columna en Clientes:**")
    st.write(df_users.isnull().sum())

    st.write("**Valores nulos por columna en Productos:**")
    st.write(df_products.isnull().sum())

    # Resumen estadístico
    st.write("**Resumen estadístico Clientes:**")
    st.write(df_users.describe())

    st.write("**Resumen estadístico Productos:**")
    st.write(df_products.describe())

    # Crear un gráfico de distribución de edades de los clientes
    st.subheader("Distribución de Edades de los Clientes")
    fig, ax = plt.subplots()
    sns.histplot(df_users['edad'], kde=True, ax=ax, color='skyblue')
    ax.set_title('Distribución de Edades')
    ax.set_xlabel('Edad')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Gráfico de categorías de productos
    st.subheader("Distribución de Categorías de Productos")
    fig, ax = plt.subplots()
    sns.countplot(x='categoria', data=df_products, ax=ax, palette='Set2')
    ax.set_title('Frecuencia de Categorías de Productos')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Gráfico de precios de productos
    st.subheader("Distribución de Precios de Productos")
    fig, ax = plt.subplots()
    sns.histplot(df_products['precio'], kde=True, ax=ax, color='green')
    ax.set_title('Distribución de Precios de Productos')
    ax.set_xlabel('Precio')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Gráfico de stock de productos
    st.subheader("Distribución de Stock de Productos")
    fig, ax = plt.subplots()
    sns.histplot(df_products['stock'], kde=True, ax=ax, color='orange')
    ax.set_title('Distribución de Stock de Productos')
    ax.set_xlabel('Stock')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)


 

    
#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------

# Filtro Final Dinámico
with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    st.markdown("""
    * Muestra un resumen dinámico del DataFrame filtrado. 
    * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
    * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
    """)
    
    # Filtro por edad de los clientes
    edad_min, edad_max = st.slider(
        "Selecciona el rango de edades de los clientes",
        min_value=int(df_users['edad'].min()),
        max_value=int(df_users['edad'].max()),
        value=(int(df_users['edad'].min()), int(df_users['edad'].max()))
    )
    df_users_filtrado = df_users[(df_users['edad'] >= edad_min) & (df_users['edad'] <= edad_max)]
    
    # Filtro por ciudad de los clientes
    ciudades = st.multiselect("Selecciona las ciudades", options=df_users['ciudad'].unique(), default=df_users['ciudad'].unique())
    df_users_filtrado = df_users_filtrado[df_users_filtrado['ciudad'].isin(ciudades)]
    
    # Filtro por categoría de productos
    categorias = st.multiselect("Selecciona las categorías de productos", options=df_products['categoria'].unique(), default=df_products['categoria'].unique())
    df_products_filtrado = df_products[df_products['categoria'].isin(categorias)]
    
    # Mostrar datos filtrados de clientes
    st.write("**Clientes Filtrados**")
    st.dataframe(df_users_filtrado)

    # Mostrar gráficos de clientes filtrados
    st.subheader("Distribución de Edades de los Clientes Filtrados")
    fig, ax = plt.subplots()
    sns.histplot(df_users_filtrado['edad'], kde=True, ax=ax, color='lightblue')
    ax.set_title('Distribución de Edades Filtradas')
    ax.set_xlabel('Edad')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Mostrar datos filtrados de productos
    st.write("**Productos Filtrados**")
    st.dataframe(df_products_filtrado)

    # Mostrar gráficos de productos filtrados
    st.subheader("Distribución de Precios de Productos Filtrados")
    fig, ax = plt.subplots()
    sns.histplot(df_products_filtrado['precio'], kde=True, ax=ax, color='lightgreen')
    ax.set_title('Distribución de Precios Filtrados')
    ax.set_xlabel('Precio')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)


