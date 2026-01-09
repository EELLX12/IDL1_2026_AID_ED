import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Análisis Estadístico y Correlaciones Interactivas Clientes")

# --- Subir CSV ---
archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])

if archivo is not None:
    try:
        df = pd.read_csv(archivo)
        # Eliminar primera columna si es RowNumber o ID
        if df.columns[0].lower() in ["rownumber", "id"]:
            df = df.iloc[:, 1:]
    except Exception as e:
        st.error(f"Error al leer el CSV: {e}")
        st.stop()
    
    # --- Variables numéricas ---
    vars_numericas = df.select_dtypes(include='number').columns.tolist()
    
    if len(vars_numericas) < 2:
        st.error("Se necesitan al menos dos variables numéricas")
        st.stop()
    
    # --- Estadísticas descriptivas con color uniforme rosa pastel ---
    st.subheader("Análisis estadístico general")
    desc = df[vars_numericas].describe().T
    color_suave = "#ffe6f0"  # rosa pastel
    styler = desc.style.set_properties(**{'background-color': color_suave, 'color': 'black'})
    st.dataframe(styler)

    # --- Selección de variable objetivo ---
    st.subheader("Correlación de varias variables con una variable objetivo")
    var_objetivo_index = len(vars_numericas) - 1
    var_objetivo = st.selectbox(
        "Selecciona variable objetivo", 
        vars_numericas, 
        index=var_objetivo_index
    )

    # --- Variables para correlacionar ---
    otras_vars = [v for v in vars_numericas if v != var_objetivo]
    default_seleccion = otras_vars[:2] if len(otras_vars) >= 2 else otras_vars
    vars_seleccionadas = st.multiselect(
        "Selecciona entre 1 y 4 variables para correlacionar con el objetivo",
        options=otras_vars,
        default=default_seleccion
    )

    if len(vars_seleccionadas) < 1 or len(vars_seleccionadas) > 4:
        st.warning("Selecciona entre 1 y 4 variables.")
    else:
        correlaciones = {}
        for var in vars_seleccionadas:
            df_filtrado = df[[var, var_objetivo]].dropna()
            correlaciones[var] = df_filtrado[var].corr(df_filtrado[var_objetivo])
        correl_df = pd.DataFrame.from_dict(correlaciones, orient='index', columns=['Correlación'])
        
        # --- Tabla de correlaciones con colores pastel ---
        st.subheader("Tabla de correlaciones")
        # Crear colormap pastel rosa
        cmap_pastel = matplotlib.colors.LinearSegmentedColormap.from_list(
            "pastel_rosa", ["#ffe6f0", "#ffccd5", "#ffb3c6"]
        )
        correl_styled = correl_df.style.background_gradient(cmap=cmap_pastel, axis=0)
        st.dataframe(correl_styled)

        # --- Scatterplots para cada variable contra el objetivo ---
        st.subheader("Scatter plots con línea de tendencia")
        pastel_colors = ["#a3c4f3", "#f7b7a3", "#c3f7a3", "#f3e9a3", "#d7a3f3"]  # paleta pastel suave
        for i, var in enumerate(vars_seleccionadas):
            df_scatter = df[[var, var_objetivo]].dropna()
            if not df_scatter.empty:
                fig = px.scatter(
                    df_scatter,
                    x=var,
                    y=var_objetivo,
                    trendline="ols",
                    title=f"{var} vs {var_objetivo}",
                    color_discrete_sequence=[pastel_colors[i % len(pastel_colors)]]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No hay suficientes datos para {var} vs {var_objetivo}")

    # --- Heatmap interactivo de correlaciones con colores pastel suaves ---
    st.subheader("Heatmap de correlaciones (colores pastel suaves)")
    corr_matrix = df[vars_numericas].corr()
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=["#ffe6f0", "#ffccd5", "#ffb3c6"]  # escala pastel suave
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- Histogramas y boxplots ---
    st.subheader("Explora tus variables")
    col1, col2 = st.columns(2)

    with col1:
        var_hist = st.selectbox("Selecciona variable para histograma", vars_numericas)
        fig_hist = px.histogram(
            df,
            x=var_hist,
            nbins=30,
            title=f"Histograma de {var_hist}",
            color_discrete_sequence=[pastel_colors[vars_numericas.index(var_hist) % len(pastel_colors)]]
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        var_box = st.selectbox("Selecciona variable para boxplot", vars_numericas, index=1)
        fig_box = px.box(
            df,
            y=var_box,
            title=f"Boxplot de {var_box}",
            points="all",
            color_discrete_sequence=[pastel_colors[vars_numericas.index(var_box) % len(pastel_colors)]]
        )
        st.plotly_chart(fig_box, use_container_width=True)

else:
    st.info("Sube un archivo CSV para comenzar")



