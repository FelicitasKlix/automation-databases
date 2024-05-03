import pandas as pd
import streamlit as st

# Importar las funciones del archivo df_cleaner.py
from df_cleaner import limpiarDataFrame, generar_utm

# Título de la aplicación
st.title("Procesamiento de Datos")

# Inputs
mes = st.text_input("Mes", "abr")
fecha = st.text_input("Fecha", "2024-04-30")
tipo = st.text_input("Tipo", "frias")

# Cargar archivos
bajada_treble = st.file_uploader("Cargar bajada-treble.csv", type="csv")
bases_calientes = st.file_uploader("Cargar bases-calientes.csv", type="csv")

# Botón para procesar datos
if st.button("Procesar Datos"):
    if bajada_treble and bases_calientes:
        # Leer los archivos cargados
        bajada_treble_df = pd.read_csv(bajada_treble)
        bases_calientes_df = pd.read_csv(bases_calientes, dtype={'PHONE': str})

        data_final_filtrado = limpiarDataFrame(bajada_treble_df, bases_calientes_df, mes, fecha, tipo)

        # Mostrar el resultado final
        st.write(data_final_filtrado)

        # Descargar el archivo CSV
        csv = data_final_filtrado.to_csv(index=False)
        st.download_button(
            label="Descargar data-final"+mes+"-"+fecha+"-"+tipo+".csv",
            data=csv,
            file_name="data-final"+mes+"-"+fecha+"-"+tipo+".csv",
            mime="text/csv",
        )
    else:
        st.warning("Por favor, carga los archivos bajada-treble.csv y bases-calientes.csv.")