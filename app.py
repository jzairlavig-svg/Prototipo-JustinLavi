# streamlit_app.py
# Dashboard: Accidentes de Tránsito en el Perú (SUTRAN)
# ✅ Funciona en GitHub / Streamlit Cloud sin errores
# Requiere: pip install streamlit pandas altair pydeck openpyxl

import streamlit as st
import pandas as pd
import altair as alt
import os

# Configuración general
st.set_page_config(page_title="Accidentes de Tránsito - Perú", layout="wide", page_icon="🚗")

st.title("🚗 Accidentes de Tránsito en el Perú (SUTRAN)")
st.markdown(
    """
    Este dashboard muestra información real sobre los **accidentes de tránsito en el Perú**,  
    basado en datos abiertos del [MTC y SUTRAN](https://datosabiertos.mtc.gob.pe).
    """
)

# ------------------------------------------------------
# 🔹 Ruta local al dataset (debe estar en /data del repo)
# ------------------------------------------------------
DATA_PATH = "data/accidentes_sutran.csv"

# ------------------------------------------------------
# 🔹 Función para cargar datos (local o remoto)
# ------------------------------------------------------
@st.cache_data(ttl=3600)
def cargar_datos(path):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, sep=";", encoding="utf-8", low_memory=False)
            return df, None
        except Exception as e:
            return None, f"Error al leer el CSV local: {e}"
    else:
        return None, f"No se encontró el archivo en la ruta: {path}"

# ------------------------------------------------------
# 🔹 Cargar dataset
# ------------------------------------------------------
with st.spinner("Cargando datos..."):
    df, err = cargar_datos(DATA_PATH)

if err or df is None:
    st.error("⚠️ No se pudo cargar el dataset real desde la ruta local.")
    st.info(err)
    st.warning("Mostrando dataset de ejemplo para visualización.")
    df = pd.DataFrame({
        "fecha": pd.date_range("2021-01-01", periods=12, freq="M"),
        "departamento": ["Lima","Junín","Cusco","Lima","Arequipa","Lima","Cusco","Piura","Lima","Loreto","Lima","Ica"],
        "modalidad": ["Choque","Despiste","Atropello","Choque","Volcadura","Choque","Atropello","Choque","Choque","Despiste","Atropello","Choque"],
        "fallecidos": [1,0,2,0,1,0,0,1,0,0,0,2],
        "heridos": [0,2,1,3,0,1,0,2,1,0,0,1],
    })

# ------------------------------------------------------
# 🔹 Preprocesamiento
# ------------------------------------------------------
df.columns = [c.lower().strip() for c in df.columns]
if "fecha" in df.columns:
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

# ------------------------------------------------------
# 🔹 Filtros
# ------------------------------------------------------
st.sidebar.header("🎛️ Filtros")

anio_min = int(df["fecha"].dt.year.min()) if "fecha" in df.columns else 2020
anio_max = int(df["fecha"].dt.year.max()) if "fecha" in df.columns else 2025
rango_anios = st.sidebar.slider("Seleccionar rango de años", anio_min, anio_max, (anio_min, anio_max))

departamentos = sorted(df["departamento"].dropna().unique()) if "departamento" in df.columns else []
deptos_sel = st.sidebar.multiselect("Departamento", departamentos)

modalidades = sorted(df["modalidad"].dropna().unique()) if "modalidad" in df.columns else []
mod_sel = st.sidebar.multiselect("Modalidad de accidente", modalidades)

df_f = df.copy()
if "fecha" in df_f.columns:
    df_f = df_f[(df_f["fecha"].dt.year >= rango_anios[0]) & (df_f["fecha"].dt.year <= rango_anios[1])]
if deptos_sel:
    df_f = df_f[df_f["departamento"].isin(deptos_sel)]
if mod_sel:
    df_f = df_f[df_f["modalidad"].isin(mod_sel)]

# ------------------------------------------------------
# 🔹 Métricas principales
# ------------------------------------------------------
st.markdown("## 📊 Métricas principales")

col1, col2, col3 = st.columns(3)
col1.metric("Registros totales", f"{len(df_f):,}")
col2.metric("Total fallecidos", f"{df_f['fallecidos'].sum():,}" if "fallecidos" in df_f else "N/A")
col3.metric("Total heridos", f"{df_f['heridos'].sum():,}" if "heridos" in df_f else "N/A")

# ------------------------------------------------------
# 🔹 Serie temporal
# ------------------------------------------------------
st.markdown("## 📈 Evolución mensual de accidentes")

if "fecha" in df_f.columns:
    df_ts = df_f.set_index("fecha").resample("M").size().reset_index(name="n_accidentes")
    chart = alt.Chart(df_ts).mark_line(point=True, color="#FF4B4B").encode(
        x="fecha:T", y="n_accidentes:Q", tooltip=["fecha:T", "n_accidentes:Q"]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No hay columna 'fecha' en el dataset.")

# ------------------------------------------------------
# 🔹 Top departamentos
# ------------------------------------------------------
st.markdown("## 🏙️ Top 10 departamentos por número de accidentes")

if "departamento" in df_f.columns:
    df_top = (
        df_f.groupby("departamento")
        .agg(accidentes=("departamento", "size"), fallecidos=("fallecidos", "sum"), heridos=("heridos", "sum"))
        .reset_index()
        .sort_values("accidentes", ascending=False)
    )
    st.table(df_top.head(10))
else:
    st.info("No hay columna 'departamento' en el dataset.")

# ------------------------------------------------------
# 🔹 Exportar datos filtrados
# ------------------------------------------------------
st.markdown("## 💾 Exportar datos filtrados")
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV filtrado", csv, "accidentes_filtrados.csv", "text/csv")

# ------------------------------------------------------
# 🔹 Notas finales
# ------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    **Notas:**
    - El dataset se carga desde `/data/accidentes_sutran.csv` (datos reales del MTC/SUTRAN).
    - Si subes tu app a Streamlit Cloud, asegúrate de incluir esa carpeta y el CSV.
    - Puedes actualizar el archivo desde [datosabiertos.mtc.gob.pe](https://datosabiertos.mtc.gob.pe).
    """
)
