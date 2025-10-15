import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Apuntes de Obstetricia", layout="centered")

# Columnas estándar
COLUMNAS = ["Fecha", "Tipo", "Tema", "Subtema", "Contenido", "Importante"]

# Cargar datos o inicializar vacío
try:
    datos = pd.read_csv("apuntes.csv")
    # Si faltan columnas, las agregamos
    for col in COLUMNAS:
        if col not in datos.columns:
            datos[col] = ""
except FileNotFoundError:
    datos = pd.DataFrame(columns=COLUMNAS)

# Glosario clínico en la barra lateral
glosario = {
    "Preeclampsia": "Hipertensión + proteinuria después de la semana 20.",
    "Corioamnionitis": "Infección de las membranas fetales.",
    "Diabetes gestacional": "Intolerancia a la glucosa durante el embarazo.",
    "Cesárea": "Intervención quirúrgica para extraer al bebé.",
    "Parto prematuro": "Nacimiento antes de la semana 37."
}
termino = st.sidebar.selectbox("📖 Glosario clínico", list(glosario.keys()))
st.sidebar.write(glosario[termino])

# Lista de temas y subtemas
temas = [
    "Preeclampsia", "Parto prematuro", "Cesárea", "Corioamnionitis",
    "Diabetes gestacional", "Hemorragia del primer trimestre",
    "Síndromes hipertensivos", "Infección intraamniótica",
    "Puerperio", "Embarazo adolescente"
]

subtemas_dict = {
    "Preeclampsia": ["Leve", "Grave", "Complicaciones"],
    "Parto prematuro": ["Causas", "Tratamiento", "Prevención"],
    "Cesárea": ["Indicaciones", "Postoperatorio", "Complicaciones"],
    "Diabetes gestacional": ["Diagnóstico", "Control", "Riesgos"],
    "Puerperio": ["Fisiológico", "Complicaciones", "Cuidados"]
}

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Nuevo apunte", "📚 Ver apuntes", "🔎 Buscar", "🧪 Modo estudio", "❓ Haz una pregunta"
])

# TAB 1: Nuevo apunte
with tab1:
    tema = st.selectbox("Selecciona el tema del apunte", temas)
    subtemas = subtemas_dict.get(tema, [])
    subtema = st.selectbox("Selecciona el subtema", subtemas) if subtemas else "General"
    contenido = st.text_area("Escribe tu apunte aquí", height=150)
    importante = st.checkbox("📌 Marcar como importante")

    if st.button("Guardar apunte"):
        if contenido.strip():
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            nuevo = pd.DataFrame([{
                "Fecha": fecha,
                "Tipo": "Apunte",
                "Tema": tema,
                "Subtema": subtema,
                "Contenido": contenido,
                "Importante": "Sí" if importante else "No"
            }])
            datos = pd.concat([datos, nuevo], ignore_index=True)
            datos.to_csv("apuntes.csv", index=False)
            st.success("✅ Apunte guardado correctamente.")
        else:
            st.warning("⚠️ El campo está vacío. Escribe algo antes de guardar.")

# TAB 2: Ver apuntes
with tab2:
    st.subheader("📚 Apuntes guardados")
    apuntes = datos[datos["Tipo"] == "Apunte"] if "Tipo" in datos else pd.DataFrame(columns=COLUMNAS)
    if not apuntes.empty:
        st.dataframe(apuntes)

        st.subheader("📊 Cantidad de apuntes por tema")
        conteo = apuntes["Tema"].value_counts().reset_index()
        conteo.columns = ["Tema", "Cantidad"]
        st.table(conteo)

        st.subheader("📌 Apuntes importantes")
        importantes = apuntes[apuntes["Importante"] == "Sí"]
        st.dataframe(importantes)

        st.download_button(
            label="📥 Descargar todos los registros en CSV",
            data=datos.to_csv(index=False).encode("utf-8"),
            file_name="apuntes_obstetricia.csv",
            mime="text/csv"
        )
    else:
        st.info("Aún no hay apuntes guardados.")

# TAB 3: Buscar
with tab3:
    st.subheader("🔎 Buscar por palabra clave")
    palabra = st.text_input("Escribe una palabra para buscar en apuntes")
    if palabra and "Contenido" in datos:
        resultados = datos[datos["Contenido"].str.contains(palabra, case=False, na=False)]
        st.dataframe(resultados)

    st.subheader("📅 Filtrar por fecha")
    fecha_filtrada = st.date_input("Selecciona una fecha")
    if "Fecha" in datos:
        filtrados = datos[datos["Fecha"].str.startswith(str(fecha_filtrada))]
        st.dataframe(filtrados)

# TAB 4: Modo estudio
with tab4:
    st.subheader("🧪 Tarjetas de repaso")
    apuntes = datos[datos["Tipo"] == "Apunte"] if "Tipo" in datos else pd.DataFrame(columns=COLUMNAS)
    if not apuntes.empty:
        for _, row in apuntes.iterrows():
            with st.expander(f"{row['Tema']} - {row['Subtema']} ({row['Fecha']})"):
                st.write(row["Contenido"])
    else:
        st.info("No hay apuntes para mostrar aún.")

# TAB 5: Haz una pregunta
with tab5:
    st.subheader("❓ Haz una pregunta clínica")
    tema = st.selectbox("Tema relacionado", temas)
    subtemas = subtemas_dict.get(tema, [])
    subtema = st.selectbox("Subtema", subtemas) if subtemas else "General"
    pregunta = st.text_area("Escribe tu pregunta aquí", height=150)
    importante = st.checkbox("📌 Marcar como importante")

    if st.button("Guardar pregunta"):
        if pregunta.strip():
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            nueva_pregunta = pd.DataFrame([{
                "Fecha": fecha,
                "Tipo": "Pregunta",
                "Tema": tema,
                "Subtema": subtema,
                "Contenido": pregunta,
                "Importante": "Sí" if importante else "No"
            }])
            datos = pd.concat([datos, nueva_pregunta], ignore_index=True)
            datos.to_csv("apuntes.csv", index=False)
            st.success("✅ Pregunta guardada correctamente.")
        else:
            st.warning("⚠️ El campo está vacío. Escribe algo antes de guardar.")

# Pie de página
st.markdown("---")
st.caption("App educativa basada en temas reales de obstetricia. Fuentes: uDocz, Docsity.")
