import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Apuntes de Obstetricia", layout="centered")

# Título principal
st.markdown("## 📘 Apuntes de Obstetricia")
st.write("Organiza tus apuntes clínicos de forma sencilla y segura.")

# Tip clínico en la barra lateral
st.sidebar.markdown("### 🧠 Tip clínico")
st.sidebar.info("La preeclampsia se caracteriza por hipertensión y proteinuria después de la semana 20.")

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

# Tabs para navegación
tab1, tab2, tab3 = st.tabs(["📝 Nuevo apunte", "📚 Ver apuntes", "🔎 Buscar"])

# TAB 1: Nuevo apunte
with tab1:
    tema = st.selectbox("Selecciona el tema del apunte", temas)
    contenido = st.text_area("Escribe tu apunte aquí", height=150)

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

# TAB 2: Ver apuntes
with tab2:
    st.subheader("📚 Apuntes guardados")
    try:
        apuntes = pd.read_csv("apuntes.csv")
        st.dataframe(apuntes)

        # Gráfico de temas más usados
        st.subheader("📊 Temas más registrados")
        conteo = apuntes["Tema"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(conteo.index, conteo.values, color="#6cace4")
        ax.set_ylabel("Cantidad de apuntes")
        plt.xticks(rotation=45)
        st.pyplot(fig)

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
            st.write("Para borrar, elimina manualmente el archivo 'apuntes.csv' desde tu carpeta.")
    except FileNotFoundError:
        st.info("Aún no hay apuntes guardados.")

# TAB 3: Buscar apuntes
with tab3:
    st.subheader("🔎 Buscar apuntes")
    palabra = st.text_input("Busca por palabra clave")
    try:
        apuntes = pd.read_csv("apuntes.csv")
        if palabra:
            resultados = apuntes[apuntes["Apunte"].str.contains(palabra, case=False, na=False)]
            st.write(f"Resultados para: '{palabra}'")
            st.dataframe(resultados)
    except FileNotFoundError:
        st.info("No hay apuntes para buscar aún.")

# Pie de página
st.markdown("---")
st.caption("App educativa basada en temas reales de obstetricia. Fuentes: uDocz, Docsity.")
