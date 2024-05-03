import pandas as pd
import streamlit as st

# Importar las funciones del archivo df_cleaner.py
from df_cleaner import limpiarDataFrame, generar_utm

# Título de la aplicación
#st.title("Procesamiento de Datos")
# Configuración de la página
st.set_page_config(page_title="Procesamiento de Datos", page_icon=":bar_chart:", layout="wide")

# Estilos personalizados
padding = 3
st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(to right, #f0f0f0, #e0e0e0);
            padding: {padding}rem;
            border-radius: 1rem;
        }}
        .title {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #333333;
            text-align: center;
            margin-bottom: 1rem;
        }}
        .input-container {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }}
        .input-label {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #555555;
            margin-bottom: 0.5rem;
        }}
        .file-uploader {{
            margin-bottom: 1rem;
        }}
        .process-button {{
            background-color: #007bff;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        .process-button:hover {{
            background-color: #0056b3;
        }}
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.markdown('<div class="title">Procesamiento de Datos</div>', unsafe_allow_html=True)

# Inputs
#mes = st.text_input("Mes", "abr")
#fecha = st.text_input("Fecha", "2024-04-30")
#tipo = st.text_input("Tipo", "frias")

# Inputs
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        mes = st.text_input("Mes", "abr", key="mes")
    with col2:
        fecha = st.text_input("Fecha", "2024-04-30", key="fecha")
    with col3:
        tipo = st.text_input("Tipo", "frias", key="tipo")


# Cargar archivos
#bajada_treble = st.file_uploader("Cargar bajada-treble.csv", type="csv")
#bases_calientes = st.file_uploader("Cargar bases-calientes.csv", type="csv")

# Cargar archivos
bajada_treble = st.file_uploader("Cargar bajada-treble.csv", type="csv", key="bajada_treble")
bases_calientes = st.file_uploader("Cargar bases-calientes.csv", type="csv", key="bases_calientes")


# Botón para procesar datos
with st.container():
    if st.button("Procesar Datos", key="process_button", className="process-button"):
        if bajada_treble and bases_calientes:
            # Leer los archivos cargados
            bajada_treble_df = pd.read_csv(bajada_treble)
            bases_calientes_df = pd.read_csv(bases_calientes, dtype={'PHONE': str})

            # Llamar a la función limpiarDataFrame
            data_final_filtrado = limpiarDataFrame(bajada_treble_df, bases_calientes_df, mes, fecha, tipo)

            # Mostrar el resultado final
            st.write(data_final_filtrado)

            # Descargar el archivo CSV
            csv = data_final_filtrado.to_csv(index=False)
            st.download_button(
                label="Descargar data-final-"+mes+"-"+fecha+"-"+tipo+".csv",
                data=csv,
                file_name="data-final-"+mes+"-"+fecha+"-"+tipo+".csv",
                mime="text/csv",
            )
        else:
            st.warning("Por favor, carga los archivos bajada-treble.csv y bases-calientes.csv.")


""" # Botón para procesar datos
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
            label="Descargar data-final-"+mes+"-"+fecha+"-"+tipo+".csv",
            data=csv,
            file_name="data-final-"+mes+"-"+fecha+"-"+tipo+".csv",
            mime="text/csv",
        )
    else:
        st.warning("Por favor, carga los archivos bajada-treble.csv y bases-calientes.csv.") """