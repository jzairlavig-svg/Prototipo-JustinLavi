import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Apuntes de Obstetricia", layout="centered")

# Título principal
st.title("📘 Apuntes de Obstetricia")
st.write("Esta aplicación te permite guardar y revisar tus apuntes sobre temas clave de obstetricia.")

# Lista de temas comunes en obstetricia
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

# Área de texto para escribir el apunte
contenido = st.text_area("Escribe tu apunte aquí", height=150)

# Botón para guardar
if st.button("Guardar apunte"):
    if contenido.strip() != "":
        nuevo = pd.DataFrame({"Tema": [tema], "Apunte": [contenido]})
        try:
            datos = pd.read_csv("apuntes.csv")
            datos = pd.concat([datos, nuevo], ignore_index=True)
        except FileNotFoundError:
            datos = nuevo
        datos.to_csv("apuntes.csv", index=False)
        st.success("✅ Apunte guardado correctamente.")
    else:
        st.warning("⚠️ El apunte está vacío. Escribe algo antes de guardar.")

# Mostrar apuntes guardados
st.subheader("📚 Apuntes guardados")
try:
    apuntes = pd.read_csv("apuntes.csv")
    st.dataframe(apuntes)
except FileNotFoundError:
    st.info("Aún no hay apuntes guardados.")

# Pie de página
st.markdown("---")
st.caption("App creada para fines educativos. Temas basados en fuentes como uDocz y Docsity.")
