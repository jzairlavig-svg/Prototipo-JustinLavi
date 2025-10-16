import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# -------------------------
# Configuración y estilo
# -------------------------
st.set_page_config(page_title="Apuntes de Obstetricia", layout="centered")

st.markdown("""
    <style>
    h1, h2, h3, h4 {
        font-family: 'Georgia', serif;
        color: #2E86C1;
    }
    .titulo {
        font-size: 28px;
        font-weight: bold;
        color: #117A65;
        text-align: center;
        margin-bottom: 20px;
    }
    .importante {
        background-color: #F9EBEA;
        border-left: 5px solid #C0392B;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'Verdana';
    }
    .normal {
        background-color: #EAF2F8;
        border-left: 5px solid #2980B9;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'Verdana';
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Constantes
# -------------------------
COLUMNS = ["Fecha", "Tipo", "Tema", "Subtema", "Contenido", "Importante"]
CSV_PATH = "apuntes.csv"

TEMAS = [
    "Preeclampsia", "Parto prematuro", "Cesárea", "Corioamnionitis",
    "Diabetes gestacional", "Hemorragia del primer trimestre",
    "Síndromes hipertensivos", "Infección intraamniótica",
    "Puerperio", "Embarazo adolescente",
]

SUBTEMAS = {
    "Preeclampsia": ["Leve", "Grave", "Complicaciones"],
    "Parto prematuro": ["Causas", "Tratamiento", "Prevención"],
    "Cesárea": ["Indicaciones", "Postoperatorio", "Complicaciones"],
    "Diabetes gestacional": ["Diagnóstico", "Control", "Riesgos"],
    "Puerperio": ["Fisiológico", "Complicaciones", "Cuidados"],
}

GLOSARIO = {
    "Preeclampsia": "Hipertensión + proteinuria después de la semana 20.",
    "Corioamnionitis": "Infección de las membranas fetales.",
    "Diabetes gestacional": "Intolerancia a la glucosa durante el embarazo.",
    "Cesárea": "Intervención quirúrgica para extraer al bebé.",
    "Parto prematuro": "Nacimiento antes de la semana 37.",
}

# -------------------------
# Utilidades de datos
# -------------------------
def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=COLUMNS)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[COLUMNS]

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    try:
        if not Path(CSV_PATH).exists():
            return pd.DataFrame(columns=COLUMNS)
        df = pd.read_csv(CSV_PATH)
        return ensure_schema(df)
    except Exception:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df: pd.DataFrame) -> None:
    df = ensure_schema(df)
    df.to_csv(CSV_PATH, index=False)

def append_record(tipo: str, tema: str, subtema: str, contenido: str, importante: bool) -> None:
    df = load_data()
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Tipo": tipo,
        "Tema": tema,
        "Subtema": subtema if subtema else "General",
        "Contenido": contenido,
        "Importante": "Sí" if importante else "No",
    }])
    df = pd.concat([df, nuevo], ignore_index=True)
    save_data(df)
    st.cache_data.clear()

# -------------------------
# Interfaz
# -------------------------
st.markdown("<div class='titulo'>📘 Apuntes de Obstetricia</div>", unsafe_allow_html=True)
st.write("Organiza tus apuntes clínicos y preguntas de forma sencilla, segura y visualmente atractiva.")

termino = st.sidebar.selectbox("📖 Glosario clínico", list(GLOSARIO.keys()))
st.sidebar.info(GLOSARIO[termino])

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Nuevo apunte", "📚 Ver apuntes", "🔎 Buscar", "🧪 Modo estudio", "❓ Haz una pregunta"
])

# -------------------------
# Tab 1: Nuevo apunte
# -------------------------
with tab1:
    modo_tema = st.radio("¿Cómo quieres ingresar el tema?", ["Seleccionar", "Escribir"])
    if modo_tema == "Seleccionar":
        tema = st.selectbox("Selecciona el tema del apunte", TEMAS)
    else:
        tema = st.text_input("Escribe el tema del apunte")

    subopciones = SUBTEMAS.get(tema, [])
    subtema = st.selectbox("Selecciona el subtema", subopciones) if subopciones else "General"

    contenido = st.text_area("Escribe tu apunte aquí", height=150)
    importante = st.checkbox("📌 Marcar como importante")

    if st.button("Guardar apunte"):
        if contenido.strip() and tema.strip():
            append_record("Apunte", tema, subtema, contenido, importante)
            st.success("✅ Apunte guardado correctamente.")
        else:
            st.warning("⚠️ El campo de tema o contenido está vacío.")

# -------------------------
# Tab 2: Ver apuntes
# -------------------------
with tab2:
    st.subheader("📚 Apuntes guardados")
    datos = load_data()
    apuntes = datos[datos["Tipo"] == "Apunte"] if not datos.empty else pd.DataFrame(columns=COLUMNS)

    if not apuntes.empty:
        for _, row in apuntes.iterrows():
            estilo = "importante" if row["Importante"] == "Sí" else "normal"
            st.markdown(f"""
                <div class="{estilo}">
                    <strong>{row['Fecha']} - {row['Tema']} ({row['Subtema']})</strong><br>
                    {row['Contenido']}
                </div>
            """, unsafe_allow_html=True)

        st.subheader("📊 Cantidad de apuntes por tema")
        conteo = (
            apuntes["Tema"].value_counts()
            .rename_axis("Tema")
            .reset_index(name="Cantidad")
        )
        st.table(conteo)

        st.download_button(
            label="📥 Descargar todos los registros en CSV",
            data=datos.to_csv(index=False).encode("utf-8"),
            file_name="apuntes_obstetricia.csv",
            mime="text/csv",
        )
    else:
        st.info("Aún no hay apuntes guardados.")

# -------------------------
# Tab 3: Buscar
# -------------------------
with tab3:
    st.subheader("🔎 Buscar por palabra clave")
    datos = load_data()
    palabra = st.text_input("Escribe una palabra para buscar en apuntes y preguntas")

    if palabra and not datos.empty:
        resultados = datos[datos["Contenido"].astype(str).str.contains(palabra, case=False, na=False)]
        st.dataframe(resultados)

    st.subheader("📅 Filtrar por fecha")
    fecha = st.date_input("Selecciona una fecha")
    if not datos.empty:
        datos["Fecha"] = datos["Fecha"].astype(str)
        filtrados = datos[datos["Fecha"].str.startswith(str(fecha))]
        st.dataframe(filtrados)

# -------------------------
# Tab 4: Modo estudio
# -------------------------
with tab4:
    st.subheader("🧪 Tarjetas de repaso")
    datos = load_data()
    apuntes = datos[datos["Tipo"] == "Apunte"] if not datos.empty else pd.DataFrame(columns=COLUMNS)

    if not apuntes.empty:
        for _, row in apuntes.iterrows():
            titulo = f"{row['Tema']} - {row['Subtema']} ({row['Fecha']})"
            with st.expander(titulo):
                st.write(row["Contenido"])
    else:
        st.info("No hay apuntes para mostrar aún.")

# -------------------------
# Tab 5: Haz una pregunta
# -------------------------
with tab5:
    st.subheader("❓ Haz una pregunta clínica")
    modo_tema_q = st.radio("¿Cómo quieres ingresar el tema?", ["Seleccionar", "Escribir"], key="modo_tema_q")

    if modo_tema_q == "Seleccionar":
        tema_q = st.selectbox("Tema relacionado", TEMAS, key="tema_q")
    else:
        tema_q = st.text_input("Escribe el
