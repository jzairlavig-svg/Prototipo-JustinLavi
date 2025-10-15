import streamlit as st
import pandas as pd
import altair as alt
import requests
from io import StringIO

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(
    page_title="Accidentes de Tránsito en el Perú",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Accidentes de Tránsito en el Perú (SUTRAN)")
st.markdown(
    "Este dashboard muestra información real sobre los **accidentes de tránsito en el Perú**, "
    "basado en datos abiertos del [MTC y SUTRAN](https://datosabiertos.mtc.gob.pe)."
)

# ----------------------------------------
# DESCARGA DE DATOS
# ----------------------------------------

@st.cache_data
def descargar_csv(url):
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return pd.read_csv(StringIO(resp.text), sep=";"), None
    except Exception as e:
        return None, str(e)

# Fuente de datos (MTC/SUTRAN)
SUTRAN_CSV_URL = "https://datosabiertos.mtc.gob.pe/sites/default/files/Accidentes%20de%20Tr%C3%A1nsito%20en%20carreteras%202020-2023%20SUTRAN.csv"

with st.spinner("Descargando dataset real..."):
    df, err = descargar_csv(SUTRAN_CSV_URL)

if df is None or df.empty:
    st.error("⚠️ No se pudo cargar el dataset real desde la URL.")
    st.info(f"Detalle del error: {err}")
    st.warning("Mostrando dataset de ejemplo para visualización.")
    df = pd.DataFrame({
        "fecha": pd.date_range("2021-01-01", periods=12, freq="M"),
        "departamento": ["Lima","Junín","Cusco","Lima","Arequipa","Lima","Cusco","Piura","Lima","Loreto","Lima","Ica"],
        "modalidad": ["Choque","Despiste","Atropello","Choque","Volcadura","Choque","Atropello","Choque","Choque","Despiste","Atropello","Choque"],
        "fallecidos": [1,0,2,0,1,0,0,1,0,0,0,2],
        "heridos": [0,2,1,3,0,1,0,2,1,0,0,1],
    })
else:
    st.success("✅ Dataset real cargado correctamente.")

# ----------------------------------------
# LIMPIEZA DE DATOS
# ----------------------------------------
if "fecha" in df.columns:
    try:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    except Exception:
        pass

# Filtros dinámicos
departamentos = sorted(df["departamento"].dropna().unique())
dep_sel = st.sidebar.multiselect("Selecciona departamentos:", departamentos, default=["Lima"])
anio_sel = st.sidebar.slider("Selecciona año:", 2020, 2024, (2021, 2023))

# Filtrado
df_filtrado = df.copy()
if "fecha" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado["fecha"].dt.year >= anio_sel[0]) &
        (df_filtrado["fecha"].dt.year <= anio_sel[1])
    ]
if "departamento" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["departamento"].isin(dep_sel)]

# ----------------------------------------
# VISUALIZACIONES
# ----------------------------------------

st.subheader("📈 Evolución de accidentes por mes")

if "fecha" in df_filtrado.columns:
    chart = (
        alt.Chart(df_filtrado)
        .mark_line(point=True)
        .encode(
            x=alt.X("yearmonth(fecha):T", title="Fecha"),
            y=alt.Y("count():Q", title="Cantidad de accidentes"),
            color="departamento:N"
        )
        .properties(height=400)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No se encontró la columna de fechas en el dataset.")

st.subheader("💥 Distribución por tipo de accidente")
if "modalidad" in df_filtrado.columns:
    tipo_chart = (
        alt.Chart(df_filtrado)
        .mark_bar()
        .encode(
            x=alt.X("modalidad:N", title="Tipo de accidente"),
            y=alt.Y("count():Q", title="Cantidad"),
            color="modalidad:N"
        )
        .properties(height=400)
    )
    st.altair_chart(tipo_chart, use_container_width=True)

# ----------------------------------------
# MÉTRICAS
# ----------------------------------------

col1, col2, col3 = st.columns(3)
total_accidentes = len(df_filtrado)
total_fallecidos = df_filtrado["fallecidos"].sum() if "fallecidos" in df_filtrado else 0
total_heridos = df_filtrado["heridos"].sum() if "heridos" in df_filtrado else 0

col1.metric("🚗 Accidentes totales", f"{total_accidentes:,}")
col2.metric("☠️ Fallecidos", f"{total_fallecidos:,}")
col3.metric("🤕 Heridos", f"{total_heridos:,}")

# ----------------------------------------
# PIE DE PÁGINA
# ----------------------------------------
st.markdown("---")
st.caption("Fuente: Ministerio de Transportes y Comunicaciones (MTC) - SUTRAN | Desarrollado por Justin Lavi 🧠")
