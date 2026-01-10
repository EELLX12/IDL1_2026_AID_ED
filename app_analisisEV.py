import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib
import numpy as np


st.set_page_config(
    page_title="Dashboard Exploratorio",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

pastel_colors = ["#a3c4f3", "#f7b7a3", "#c3f7a3", "#f3e9a3", "#d7a3f3"]

# ===============================
# CARGA DE ARCHIVO
# ===============================
st.title("📊 Dashboard de Análisis Exploratorio -  Pedidos Juyo SAC")

archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is None:
    st.info("⬆️ Sube un archivo CSV para comenzar")
    st.stop()

try:
    df = pd.read_csv(archivo)
except Exception as e:
    st.error(f"❌ Error al leer el CSV: {e}")
    st.stop()


# VARIABLES
# ===============================
vars_numericas = df.select_dtypes(include="number").columns.tolist()
vars_categoricas = df.select_dtypes(exclude="number").columns.tolist()


# ANÁLISIS ESTADÍSTICO
# ===============================
st.header("📌 1. Análisis estadístico general")

if len(vars_numericas) < 1:
    st.warning("No hay variables numéricas disponibles")
else:
    desc = df[vars_numericas].describe().T
    st.dataframe(
        desc.style
        .format("{:.2f}")
        .set_properties(background_color="#ffe6f0", color="black"),
        use_container_width=True
    )


#DISTRIBUCIÓN DE VARIABLES
# ===============================
st.header("📈 2. Distribución de variables numéricas")

col1, col2 = st.columns(2)

with col1:
    var_hist = st.selectbox("Selecciona variable (Histograma)", vars_numericas)
    fig_hist = px.histogram(
        df,
        x=var_hist,
        nbins=30,
        color_discrete_sequence=["#a3c4f3"],
        title=f"Distribución de {var_hist}"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    var_box = st.selectbox("Selecciona variable (Boxplot)", vars_numericas, index=0)
    fig_box = px.box(
        df,
        y=var_box,
        points="all",
        color_discrete_sequence=["#f7b7a3"],
        title=f"Boxplot de {var_box}"
    )
    st.plotly_chart(fig_box, use_container_width=True)

#  VARIABLES CUALITATIVAS
# ===============================
st.header(" 3. Variables cualitativas")

if len(vars_categoricas) == 0:
    st.info("No hay variables cualitativas en el dataset")
else:
    var_cat = st.selectbox("Selecciona variable cualitativa", vars_categoricas)
    tipo_grafico = st.radio("Tipo de gráfico", ["Barras", "Pastel"], horizontal=True)

    conteo = df[var_cat].value_counts().reset_index()
    conteo.columns = [var_cat, "Frecuencia"]

    if tipo_grafico == "Barras":
        fig_bar = px.bar(
            conteo,
            x=var_cat,
            y="Frecuencia",
            color_discrete_sequence=["#c3f7a3"],
            title=f"Distribución de {var_cat}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        fig_pie = px.pie(
            conteo,
            names=var_cat,
            values="Frecuencia",
            color_discrete_sequence=pastel_colors,
            title=f"Proporción de {var_cat}"
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# CORRELACIONES
# ===============================
st.header("🔗 4. Correlaciones entre variables numéricas")

if len(vars_numericas) < 2:
    st.warning("Se necesitan al menos dos variables numéricas")
else:
    var_objetivo = st.selectbox(
        "Selecciona variable objetivo",
        vars_numericas,
        index=len(vars_numericas) - 1
    )

    otras_vars = [v for v in vars_numericas if v != var_objetivo]

    vars_sel = st.multiselect(
        "Selecciona entre 1 y 4 variables",
        otras_vars,
        default=otras_vars[:2]
    )

    if 1 <= len(vars_sel) <= 4:
        correl_df = (
            df[vars_sel + [var_objetivo]]
            .corr()[var_objetivo]
            .drop(var_objetivo)
            .to_frame("Correlación")
        )

        cmap_pastel = matplotlib.colors.LinearSegmentedColormap.from_list(
            "pastel", ["#ffe6f0", "#ffccd5", "#ffb3c6"]
        )

        st.subheader("📋 Tabla de correlaciones")
        st.dataframe(
            correl_df.style
            .format("{:.2f}")
            .background_gradient(cmap=cmap_pastel),
            use_container_width=True
        )

        st.subheader("📉 Scatter plots con tendencia")
        for i, var in enumerate(vars_sel):
            fig = px.scatter(
                df,
                x=var,
                y=var_objetivo,
                trendline="ols",
                color_discrete_sequence=[pastel_colors[i % len(pastel_colors)]],
                title=f"{var} vs {var_objetivo}"
            )
            st.plotly_chart(fig, use_container_width=True)


#  HEATMAP
# ===============================
st.header("🔥 5. Heatmap de correlaciones")

if len(vars_numericas) >= 2:
    fig_heatmap = px.imshow(
        df[vars_numericas].corr(),
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=["#ffe6f0", "#ffccd5", "#ffb3c6"]
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("✨ **Dashboard generado con Streamlit**")
