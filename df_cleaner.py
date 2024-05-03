import pandas as pd

def limpiarDataFrame(bajada_treble, bases_calientes, mes, fecha, tipo):

    # Filtrar las filas donde el estado sea "DELIVERED"
    filas_entregadas = bajada_treble.loc[bajada_treble["Estado"] == "DELIVERED"]

    # Seleccionar las columnas específicas que quieres verificar
    columnas_a_verificar = [
        bajada_treble.columns[10],
        bajada_treble.columns[15],
        bajada_treble.columns[16],
        bajada_treble.columns[17],
        bajada_treble.columns[18],
        bajada_treble.columns[19]
    ]

    # Filtrar las filas en filas_entregadas donde hay NaN en las columnas seleccionadas
    filas_con_nan = filas_entregadas.loc[filas_entregadas[columnas_a_verificar].isna().all(axis=1)]

    # Creamos el dataframe final
    data = {'Codigo de pais': filas_con_nan['Codigo de pais'], 'Celular': filas_con_nan['Celular']}
    data_final = pd.DataFrame(data)

    # Paso 1: Concatenar 'Codigo de pais' y 'Celular' en bajada_treble
    bajada_treble['Codigo de pais'] = bajada_treble['Codigo de pais'].astype(str)
    bajada_treble['PHONE'] = bajada_treble['Codigo de pais'] + bajada_treble['Celular'].astype(str)

    # Paso 2: Unir ambos dataframes
    df_final = pd.concat([bases_calientes, bajada_treble], ignore_index=True)

    # Paso 3: Eliminar filas duplicadas basadas en la columna 'PHONE'
    df_final = df_final.drop_duplicates(subset='PHONE')

    # Paso 4: Seleccionar solo las columnas 'PHONE' y 'Codigo de pais'
    df_final = df_final[['Codigo de pais', 'PHONE']]

    data_final = pd.DataFrame({'Codigo de pais': None, 'PHONE': df_final['PHONE']})

    # Convertir los valores de la columna 'PHONE' a cadenas de texto
    data_final['PHONE'] = data_final['PHONE'].astype(str)

    # Aplicar una función lambda para extraer los dos primeros dígitos y asignarlos a 'Codigo de pais'
    data_final['Codigo de pais'] = data_final['PHONE'].apply(lambda x: x[:2])

    # Eliminar los dos primeros dígitos de 'PHONE'
    data_final['PHONE'] = data_final['PHONE'].apply(lambda x: x[2:])

    # Aplicar la función a las filas del DataFrame para crear la columna 'utm'
    #data_final['utm'] = data_final.apply(generar_utm, axis=1)
    data_final['utm'] = data_final.apply(lambda row: generar_utm(row, mes, fecha, tipo), axis=1)
    data_final.dropna()
    # Lista de valores permitidos en la columna 'Codigo de pais'
    valores_permitidos = ["50", "51", "52", "54", "55", "56", "57", "59"]

    # Seleccionar las filas que contienen alguno de los valores permitidos en 'Codigo de pais'
    data_final_filtrado = data_final[data_final['Codigo de pais'].isin(valores_permitidos)]

    # Hacer una copia del DataFrame antes de ordenarlo
    data_final_filtrado = data_final_filtrado.copy()

    # Ordenar el DataFrame por 'Codigo de pais'
    data_final_filtrado.sort_values(by='Codigo de pais', inplace=True)

    return data_final_filtrado


# Función para generar la cadena UTM
def generar_utm(row, mes, fecha, tipo):
    codigo_pais = row['Codigo de pais']
    if codigo_pais == '55':  # Brasil
        idioma = "pt"
        pais = "br"
    if codigo_pais == '59':
      if row['PHONE'].startswith('3'):  # Ecuador
            pais = "ec"
            idioma = "es"
      elif row['PHONE'].startswith('8'):  # Uruguay
            pais = "uy"
            idioma = "es"
    else:
        # Mapeo de códigos de país a sus respectivas abreviaturas
        codigos_pais = {
            "54": "ar",
            "56": "cl",
            "50": "cr",
            "57": "co",
            "51": "pe",
            "52": "mx"
        }
        pais = codigos_pais.get(codigo_pais, "")
        idioma = "es"
    return f"{idioma}-{pais}?utm_referral_code=rappialiados&utm_source=treble&utm_medium=whatsapp&utm_campaign={tipo}-{mes}_{pais}_{fecha}"