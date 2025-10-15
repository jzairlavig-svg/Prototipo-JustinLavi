# streamlit_app.py
# Streamlit app: Accidentes de tránsito en Perú (usa datasets oficiales SUTRAN / ONSV / INEI)
# Ejecutar: pip install streamlit pandas altair folium pydeck requests openpyxl
# Luego: streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import altair as alt
import requests
from io import BytesIO
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Accidentes de Tránsito - Perú", page_icon="🚦")

st.title("Accidentes de Tránsito en Perú — visualización (datos abiertos)")

st.markdown(
    """
    **Fuentes (cargadas automáticamente):**
    - SUTRAN / Plataforma Nacional de Datos Abiertos (dataset "Accidentes de tránsito en carreteras").  
    - Observatorio Nacional de Seguridad Vial (ONSV) / INEI (boletines) según corresponda.
    """
)

# -------- Usuario: URLs de datasets (editar si tienes otra versión) --------
SUTRAN_CSV_URL = (
    "https://datosabiertos.gob.pe/sites/default/files/Accidentes%20de%20tr%C3%A1nsito%20en%20carreteras-2020-2021-Sutran.csv"
)
# ONSV histórico (si quieres usarlo, la web publica recursos; aquí se deja como referencia)
ONSV_HIST_URL = "https://www.onsv.gob.pe/datosabiertos"  # página con recursos (xlsx/csv) -> ver explicación

# -------- Funciones auxiliares --------
@st.cache_data(ttl=3600)
def descargar_csv(url):
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        # intenta inferir si es csv o excel
        content_type = resp.headers.get("content-type", "")
        if "text/csv" in content_type or url.lower().endswith(".csv"):
            df = pd.read_csv(BytesIO(resp.content), encoding="utf-8", low_memory=False)
        else:
            # intentar excel
            df = pd.read_excel(BytesIO(resp.content))
        return df, None
    except Exception as e:
        return None, str(e)

# -------- Descargar dataset SUTRAN --------
st.sidebar.header("Configuración / Fuentes")
st.sidebar.write("Dataset por defecto: SUTRAN (Datos Abiertos). Puedes cambiar la URL si tienes otra versión.")

csv_url = st.sidebar.text_input("URL CSV (SUTRAN)", SUTRAN_CSV_URL)

with st.spinner("Descargando dataset..."):
    df, err = descargar_csv(csv_url)

if err is not None or df is None:
    st.error("No se pudo descargar o parsear el CSV desde la URL indicada.")
    st.info("Error técnico: " + (err or "desconocido"))
    st.warning("Cargando ejemplo sintético a modo demostración (revisa la URL o descarga el csv manualmente).")
    # Crear pequeño ejemplo de estructura esperada
    df = pd.DataFrame({
        "fecha": pd.date_range("2021-01-01", periods=12, freq="M"),
        "departamento": ["Lima","Junin","Cusco","Lima","Arequipa","Lima","Cusco","Piura","Lima","Loreto","Lima","Ica"],
        "modalidad": ["Choque","Despiste","Atropello","Choque","Volcadura","Choque","Atropello","Choque","Choque","Despiste","Atropello","Choque"],
        "fallecidos": [1,0,2,0,1,0,0,1,0,0,0,2],
        "heridos": [0,2,1,3,0,1,0,2,1,0,0,1],
        # si hay lat/lon: 'lat','lon'
    })

# -------- Preprocesado básico --------
# normalizar nombres de columnas comunes (intentar detectar)
df_cols = [c.lower().strip() for c in df.columns]
col_map = {original: col for original, col in zip(df.columns, df_cols)}

# renombrar para uso interno
df = df.rename(columns=col_map)

# parsear fecha
if "fecha" in df.columns:
    try:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    except:
        pass

# columnas útiles por defecto:
for col in ["departamento", "modalidad", "fallecidos", "heridos", "fecha"]:
    if col not in df.columns:
        st.warning(f"El dataset parece no tener columna esperada: '{col}'. Adapta el código según tu CSV.")

# limpiar filas sin fecha
if "fecha" in df.columns:
    df = df[~df["fecha"].isna()]

# -------- Sidebar: filtros --------
st.sidebar.subheader("Filtros")
anio_min = int(df["fecha"].dt.year.min()) if "fecha" in df.columns else 2020
anio_max = int(df["fecha"].dt.year.max()) if "fecha" in df.columns else 2025
selected_years = st.sidebar.slider("Año (rango)", anio_min, anio_max, (anio_min, anio_max))
selected_dept = st.sidebar.multiselect(
    "Departamento (filtrar)", sorted(df["departamento"].dropna().unique())[:50], default=None
)
modalidades = df["modalidad"].dropna().unique() if "modalidad" in df.columns else []
selected_modalidad = st.sidebar.multiselect("Modalidad", sorted(modalidades), default=None)

# aplicar filtros
df_filtered = df.copy()
if "fecha" in df_filtered.columns:
    df_filtered = df_filtered[
        (df_filtered["fecha"].dt.year >= selected_years[0]) &
        (df_filtered["fecha"].dt.year <= selected_years[1])
    ]
if selected_dept:
    df_filtered = df_filtered[df_filtered["departamento"].isin(selected_dept)]
if selected_modalidad:
    df_filtered = df_filtered[df_filtered["modalidad"].isin(selected_modalidad)]

st.markdown("## Vista rápida de los datos filtrados")
st.dataframe(df_filtered.head(200))

# -------- Métricas rápidas --------
st.markdown("## Métricas principales")
col1, col2, col3 = st.columns(3)
with col1:
    total_acc = len(df_filtered)
    st.metric("Registros (accidentes)", f"{total_acc:,}")
with col2:
    total_falls = int(df_filtered["fallecidos"].sum()) if "fallecidos" in df_filtered.columns else "N/A"
    st.metric("Fallecidos (sum)", f"{total_falls:,}" if isinstance(total_falls, int) else total_falls)
with col3:
    total_inj = int(df_filtered["heridos"].sum()) if "heridos" in df_filtered.columns else "N/A"
    st.metric("Heridos (sum)", f"{total_inj:,}" if isinstance(total_inj, int) else total_inj)

# -------- Serie temporal (por mes) --------
st.markdown("## Serie temporal (accidentes por mes)")
if "fecha" in df_filtered.columns:
    df_ts = df_filtered.set_index("fecha").resample("M").size().reset_index(name="n_accidentes")
    chart = alt.Chart(df_ts).mark_line(point=True).encode(
        x=alt.X("fecha:T", title="Fecha"),
        y=alt.Y("n_accidentes:Q", title="Número de accidentes")
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No hay columna 'fecha' para crear la serie temporal.")

# -------- Top departamentos --------
st.markdown("## Top departamentos por número de accidentes")
if "departamento" in df_filtered.columns:
    df_dept = df_filtered.groupby("departamento").agg(
        accidentes=("departamento","size"),
        fallecidos=("fallecidos","sum") if "fallecidos" in df_filtered.columns else pd.NamedAgg(column="departamento", aggfunc="size"),
        heridos=("heridos","sum") if "heridos" in df_filtered.columns else pd.NamedAgg(column="departamento", aggfunc="size"),
    ).reset_index().sort_values("accidentes", ascending=False)
    st.table(df_dept.head(10))
else:
    st.info("No hay columna 'departamento' para agrupar.")

# -------- Mapa (si hay lat/lon) --------
st.markdown("## Mapa (si el dataset incluye coordenadas geográficas)")
if ("lat" in df_filtered.columns and "lon" in df_filtered.columns) or ("latitude" in df_filtered.columns and "longitude" in df_filtered.columns):
    lat_col = "lat" if "lat" in df_filtered.columns else "latitude"
    lon_col = "lon" if "lon" in df_filtered.columns else "longitude"
    map_df = df_filtered.dropna(subset=[lat_col, lon_col])
    if not map_df.empty:
        st.map(map_df[[lat_col, lon_col]])
        st.success("Mapa cargado (Streamlit map). Para mapas más ricos usa pydeck/folium).")
    else:
        st.info("No se encontraron coordenadas en las filas filtradas.")
else:
    st.info("No se detectaron columnas de lat/lon en el dataset. Si existen con otros nombres, renómbralas a 'lat'/'lon' o 'latitude'/'longitude'.")

# -------- Exportar filtro actual a CSV --------
st.markdown("### Exportar")
csv_export = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV filtrado", csv_export, file_name="accidentes_filtrados.csv", mime="text/csv")

st.markdown("---")
st.markdown(
    "### Notas:\n"
    "- Revisa la **estructura de columnas** de tu CSV real y adapta los nombres en el script si fuera necesario.\n"
    "- En la web del ONSV hay recursos separados (histórico 2008-2023, siniestros fatales 2021-2023, etc.).\n"
    "- Si quieres, puedo adaptar el diseño (mapa con clustering, filtros más avanzados o dashboard en multipage)."
)
