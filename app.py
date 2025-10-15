import streamlit as st
import pandas as pd
import plotly.express as px

# 1. DATOS REALES DE ACCIDENTES DE TRÁNSITO EN PERÚ (Fuente: MTC/ONVS 2023)
# Estos datos se basan en cifras consolidadas reportadas por el Ministerio de Transporte y Comunicaciones (MTC)
# y el Observatorio Nacional de Seguridad Vial (ONSV) para el año 2023.

# Cifras de resumen nacional 2023:
ACCIDENTES_2023 = 87083
FALLECIDOS_2023 = 3316
LESIONADOS_2023 = 58000

# Distribución porcentual aproximada por factor y causa principal (Fuente: ONSV 2017-2022/2023)
# Se usa un sample de datos para crear el DataFrame
data_factores = {
    'Factor': ['Humano', 'Vehículo', 'Infraestructura', 'Otros'],
    'Porcentaje (%)': [74, 11, 10, 5],
    'Accidentes (Estimado)': [
        int(ACCIDENTES_2023 * 0.74), 
        int(ACCIDENTES_2023 * 0.11), 
        int(ACCIDENTES_2023 * 0.10), 
        int(ACCIDENTES_2023 * 0.05)
    ]
}
df_factores = pd.DataFrame(data_factores)

# Principales causas vinculadas al Factor Humano (Más del 60% de los siniestros)
data_causas = {
    'Causa': ['Imprudencia del conductor', 'Exceso de velocidad', 'Ebriedad del conductor', 'Desacato de señales (Conductor)'],
    'Porcentaje (%)': [28, 26, 7, 5], # Porcentajes reportados por MTC 2023
    'Fallecidos (Estimado)': [
        int(FALLECIDOS_2023 * 0.28),
        int(FALLECIDOS_2023 * 0.26),
        int(FALLECIDOS_2023 * 0.07),
        int(FALLECIDOS_2023 * 0.05)
    ]
}
df_causas = pd.DataFrame(data_causas)


# 2. CONFIGURACIÓN DE LA PÁGINA STREAMLIT
st.set_page_config(
    page_title="Accidentes de Tránsito en Perú", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🇵🇪 Análisis de Siniestros Viales en Perú")
st.markdown("Datos basados en cifras oficiales del **Observatorio Nacional de Seguridad Vial (ONSV)** y el **MTC** para el año **2023**.")

# 3. METRICAS CLAVE
st.header("Cifras Nacionales (2023)")
col1, col2, col3 = st.columns(3)

col1.metric("Accidentes Totales Registrados", f"{ACCIDENTES_2023:,}")
col2.metric("Fallecidos en Siniestros Viales", f"{FALLECIDOS_2023:,}")
col3.metric("Lesionados", f"{LESIONADOS_2023:,}")

st.divider()

# 4. VISUALIZACIÓN POR FACTOR DE SINIESTRALIDAD
st.header("Distribución por Factor de Siniestralidad")

# Gráfico de Factores (Circular)
fig_factores = px.pie(
    df_factores, 
    values='Porcentaje (%)', 
    names='Factor', 
    title='Principal Factor Causal de Siniestros Viales (2023)',
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_factores.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))

st.plotly_chart(fig_factores, use_container_width=True)

st.markdown(
    """
    ⚠️ **Conclusión Clave:** Alrededor del **74%** de los siniestros están directamente vinculados al **factor humano**, 
    subrayando la urgencia de la educación y la fiscalización vial.
    """
)
st.divider()

# 5. VISUALIZACIÓN POR CAUSAS ESPECÍFICAS
st.header("Causas Principales del Factor Humano (Fallecidos)")

# Gráfico de Causas (Barras)
fig_causas = px.bar(
    df_causas.sort_values(by='Fallecidos (Estimado)', ascending=False),
    x='Causa',
    y='Fallecidos (Estimado)',
    text='Fallecidos (Estimado)',
    title='Estimación de Fallecidos por Causa Principal (2023)',
    color='Causa',
    color_discrete_sequence=px.colors.qualitative.T10
)
fig_causas.update_traces(textposition='outside')
fig_causas.update_layout(yaxis_title="Número Estimado de Fallecidos", xaxis_title="")

st.plotly_chart(fig_causas, use_container_width=True)

# 6. TABLA DE DATOS
st.subheader("Tabla de Datos Detallados (Estimados)")
st.dataframe(df_causas)
