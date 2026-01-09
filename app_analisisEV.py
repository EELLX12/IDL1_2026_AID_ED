import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Análisis estadístico y  Visualización de Clientes")

#cargar el archivo
archivo = st.file_uploader("Sube el archivo CSV", type=["csv"])
if archivo is not None:
    df = pd.read_csv(archivo)
    
    st.subheader("Variables numéricas disponibles")
    vars_numericas = df.select_dtypes(include='number').columns.tolist()
    st.write(vars_numericas)

    var_x = st.selectbox("Selecciona la primera variable", vars_numericas)
    var_y = st.selectbox("Selecciona la segunda variable", vars_numericas)

    if var_x != var_y:
        correlacion = df[var_x].corr(df[var_y], method='pearson')

        st.metric(
            label="Correlación entre {var_x} y {var_y}",
            value=round(correlacion, 3)
        )

        #Interpretación automática
        if abs(correlacion) >= 0.7:
            st.warning("Correlación fuerte")
        elif abs(correlacion) >= 0.4:
            st.info("Correlación moderada")
        elif abs(correlacion) >= 0.2:
            st.success("Correlación débil")
        else:
            st.write("Correlación nula o inexistente")

        st.info("Interpretación: {interpretacion}")

    else:
        st.error("Seleccione dos variables diferentes")
else:
    st.error("Sube un archivo CSV")