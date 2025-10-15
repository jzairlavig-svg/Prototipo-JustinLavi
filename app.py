import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Apuntes de Obstetricia", layout="centered")

st.title("📘 Apuntes de Obstetricia")
st.write("Organiza tus apuntes clínicos de forma sencilla y segura.")

# Lista de temas
temas = [
    "Preeclampsia",
    "Parto prematuro",
    "Cesárea",
    "Corioamnionitis",
    "Diabetes gestacional",
    "Hemorragia del primer trimestre",
    "Síndromes hipertensivos",
    "Infección intraamniótica",
    "Puerperio",
    "Embarazo adolescente"
]

# Selección de tema
tema = st.selectbox("Selecciona el tema del apunte", temas)

# Área de texto
contenido = st.text_area("Escribe tu apunte aquí", height=150)

# Guardar apunte
if st.button("Guardar apunte"):
    if contenido.strip() != "":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        nuevo = pd.DataFrame({
            "Fecha": [fecha],
            "Tema": [tema],
            "Apunte": [contenido]
        })
        try:
            datos = pd.read_csv("apuntes.csv")
            datos = pd.concat([datos, nuevo], ignore_index=True)
        except FileNotFoundError:
            datos = nuevo
        datos.to_csv("apuntes.csv", index=False)
        st.success("✅ Apunte guardado correctamente.")
    else:
        st.warning("⚠️ El campo está vacío. Escribe algo antes de guardar.")

# Mostrar apuntes guardados
st.subheader("📚 Apuntes guardados")
try:
    apuntes = pd.read_csv("apuntes.csv")
    st.dataframe(apuntes)

    # Buscador
    st.subheader("🔎 Buscar apuntes")
    palabra = st.text_input("Buscar por palabra clave")
    if palabra:
        resultados = apuntes[apuntes["Apunte"].str.contains(palabra, case=False, na=False)]
        st.write(f"Resultados para: '{palabra}'")
        st.dataframe(resultados)

    # Descargar CSV
    st.download_button(
        label="📥 Descargar apuntes en CSV",
        data=apuntes.to_csv(index=False).encode("utf-8"),
        file_name="apuntes_obstetricia.csv",
        mime="text/csv"
    )

    # Borrar apuntes
    if st.button("🧹 Borrar todos los apuntes"):
        st.warning("⚠️ Esta acción eliminará todos los apuntes guardados.")
        st.write("Si estás seguro, elimina manualmente el archivo 'apuntes.csv' desde tu carpeta.")
except FileNotFoundError:
    st.info("Aún no hay apuntes guardados.")

# Pie de página
st.markdown("---")
st.caption("App educativa basada en temas reales de obstetricia. Fuentes: uDocz, Docsity.")
