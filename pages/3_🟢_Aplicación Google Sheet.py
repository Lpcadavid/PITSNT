import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

# Descripción para el usuario
st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Hoja1", los procesa con Pandas y actualiza una segunda hoja llamada "Hoja2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.
""")

# Configuración de acceso a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = st.text_input("ID hoja de cálculo")
RANGE1 = "Hoja 1!A:F"  # Rango extendido para capturar todas las columnas necesarias.
RANGE2 = "Hoja 2!A:F"  # El rango para actualizar la Hoja 2.

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Función para leer la Hoja 1
def read_sheet():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    # Convertir los datos en un DataFrame de Pandas
    df = pd.DataFrame(values[1:], columns=values[0])  # La primera fila como encabezado
    return df

# Función para actualizar la Hoja 2
def update_sheet(df):
    # Limpiar los datos reemplazando NaN por cadenas vacías
    df_cleaned = df.fillna('')  # Reemplazar NaN con cadenas vacías
    body = {'values': df_cleaned.values.tolist()}  # Convertir el DataFrame a lista de listas
    
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

# Botón para leer y procesar los datos
if st.button("Analizar datos de Google Sheet"):
    # Leer datos de la Hoja 1
    df = read_sheet()
    st.header("Datos Hoja 1")
    st.dataframe(df)
    
    # Verificar las columnas que están presentes en el DataFrame
    st.write("Columnas disponibles en el DataFrame:", df.columns)
    
    # Asegurarnos de que las columnas estén bien formateadas y sin espacios
    df.columns = df.columns.str.strip()  # Eliminar espacios al principio y final de los nombres de las columnas
    
    # Verificar si las columnas 'Cantidad', 'Precio' y 'Ventas' existen
    if 'Cantidad' in df.columns and 'Precio' in df.columns and 'Ventas' in df.columns:
        # Convertir las columnas 'Cantidad', 'Precio' y 'Ventas' a valores numéricos si es necesario
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
        df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce')
        
        # Crear una columna de "Ventas Totales" que será el producto de Precio * Cantidad
        df['Ventas Totales'] = df['Precio'] * df['Cantidad']
        
        # Agrupar los datos por Ciudad y Producto y calcular las Ventas Totales
        df_agrupado = df.groupby(['Ciudad', 'Producto']).agg({'Ventas Totales': 'sum'}).reset_index()
        
        # Agrupar los datos por Ciudad y calcular las Ventas Totales
        df_agrupado_ciudad = df.groupby('Ciudad').agg({'Ventas Totales': 'sum'}).reset_index()
        
        # Crear los títulos para cada sección
        titulo_ciudad_producto = pd.DataFrame([['Resultados de Ventas Totales por Ciudad y Producto']], columns=['Título'])
        titulo_ciudad = pd.DataFrame([['Resultados de Ventas Totales por Ciudad']], columns=['Título'])
        
        # Concatenar los títulos con los resultados correspondientes
        df_final = pd.concat([titulo_ciudad_producto, df_agrupado, titulo_ciudad, df_agrupado_ciudad], axis=0, ignore_index=True)
        
        # Mostrar los resultados
        st.header("Ventas Totales por Ciudad y Producto")
        st.dataframe(df_agrupado)
        
        st.header("Ventas Totales por Ciudad")
        st.dataframe(df_agrupado_ciudad)

        # Actualizar la Hoja 2 con los datos procesados
        result = update_sheet(df_final)
        st.success(f"Hoja 2 actualizada. {result.get('updatedCells')} celdas actualizadas.")
        
        # Mostrar el DataFrame actualizado
        st.header("Datos actualizados en Hoja 2")
        st.dataframe(df_final)
        
    else:
        st.error("No se encuentran las columnas 'Cantidad', 'Precio' o 'Ventas' en los datos. Verifique la hoja de cálculo.")
