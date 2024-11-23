import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

df = pd.read_csv('./static/datasets/ventas.csv')


tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Análisis Exploratorio", "Filtro Final Dinámico"])

  

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
#----------------------------------------------------------
#Análisis Exploratorio
#----------------------------------------------------------
with tab_Análisis_Exploratorio:
    st.title("Análisis Exploratorio")
    st.markdown("""
    ### Descripción del Dataset:
    A continuación, realizaremos un análisis inicial del dataset cargado.
    """)

    # Muestra las primeras 5 filas del DataFrame
    st.subheader("Primeras 5 filas del dataset")
    st.dataframe(df.head())

    # Muestra la cantidad de filas y columnas
    st.subheader("Dimensiones del Dataset")
    st.write(f"El dataset contiene {df.shape[0]} filas y {df.shape[1]} columnas.")

    # Muestra los tipos de datos de cada columna
    st.subheader("Tipos de Datos de las Columnas")
    st.write(df.dtypes)

    # Identifica y muestra las columnas con valores nulos
    st.subheader("Columnas con valores nulos")
    st.write(df.isnull().sum())

    # Muestra un resumen estadístico de las columnas numéricas
    st.subheader("Resumen Estadístico")
    st.write(df.describe())

    # Muestra la frecuencia de valores únicos para una columna categórica seleccionada
    columna_categorica = st.selectbox("Selecciona una columna categórica para ver la frecuencia de valores:", df.select_dtypes(include=['object']).columns)
    st.subheader(f"Frecuencia de valores para la columna '{columna_categorica}'")
    st.write(df[columna_categorica].value_counts())

    # Otra información importante
    st.markdown("""
    Además, a continuación podemos analizar distribuciones o correlaciones más detalladas si lo deseas.
    """)
    
    
#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------

with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.title("Análisis de Ventas Interactivo")
 
# Carga de Datos
        try:
            # Cargar el dataset desde el archivo cargado
            df = pd.read_csv('./static/datasets/ventas.csv')
            st.success("Datos cargados exitosamente.")
        except FileNotFoundError:
            st.error("No se pudo encontrar el archivo 'ventas.csv'. Verifica la ruta.")
            st.stop()  # Detener la ejecución si no se encuentran los datos
        
        # Renombrar columnas para que coincidan con el código original
        df.rename(columns={'Producto': 'articulo', 'Cantidad': 'cantidad', 'Ciudad': 'ciudad', 'Precio': 'precio'}, inplace=True)
        
        # Verificar columnas esenciales
        if not {'articulo', 'cantidad', 'ciudad'}.issubset(df.columns):
            st.error("El dataset no contiene las columnas necesarias ('articulo', 'cantidad', 'ciudad').")
            st.stop()
        
        # Filtro por ciudad
        ciudades = df['ciudad'].unique()
        ciudad_seleccionada = st.multiselect("Selecciona una o más ciudades para el análisis:", ciudades, default=ciudades)
        
        # Filtro por artículo
        articulos = df['articulo'].unique()
        articulo_seleccionado = st.multiselect("Selecciona uno o más artículos para el análisis:", articulos, default=articulos)
        
        # Filtrar el dataset según selección
        df_filtrado = df[(df['ciudad'].isin(ciudad_seleccionada)) & (df['articulo'].isin(articulo_seleccionado))]
        
        # Selección del tipo de gráfico
        tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Barras", "Pastel"])
        
        # Generar gráfico interactivo
        st.subheader("Artículos Más Vendidos (Personalizado)")
        ventas_articulos = df_filtrado.groupby("articulo")["cantidad"].sum().sort_values(ascending=False)
        
        if tipo_grafico == "Barras":
            fig_bar = px.bar(ventas_articulos, x=ventas_articulos.index, y=ventas_articulos.values,
                            title="Top Artículos Vendidos", labels={'x': 'Artículo', 'y': 'Cantidad'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            fig_pie = px.pie(ventas_articulos, values=ventas_articulos.values, names=ventas_articulos.index,
                            title="Distribución de Ventas por Artículo")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Gráfico de ventas por ciudad
        st.subheader("Participación de Ventas por Ciudad (Personalizado)")
        ventas_ciudad = df_filtrado.groupby("ciudad")["cantidad"].sum()
        
        if tipo_grafico == "Barras":
            fig_bar_ciudad = px.bar(ventas_ciudad, x=ventas_ciudad.index, y=ventas_ciudad.values,
                                    title="Distribución de Ventas por Ciudad", labels={'x': 'Ciudad', 'y': 'Cantidad'})
            st.plotly_chart(fig_bar_ciudad, use_container_width=True)
        else:
            fig_pie_ciudad = px.pie(ventas_ciudad, values=ventas_ciudad.values, names=ventas_ciudad.index,
                                    title="Distribución de Ventas por Ciudad")
            st.plotly_chart(fig_pie_ciudad, use_container_width=True)