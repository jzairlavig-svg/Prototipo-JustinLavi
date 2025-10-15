import streamlit as st
import json
import pandas as pd

# -------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------
st.set_page_config(page_title="Apuntes de Obstetricia 🩺", page_icon="🩺", layout="centered")

# -------------------------------
# TÍTULO Y DESCRIPCIÓN
# -------------------------------
st.markdown("""
    <h1 style='text-align: center; color: #D63384;'>🩺 Apuntes de Obstetricia</h1>
    <p style='text-align: center; font-size:18px;'>
    Material académico con datos reales del MINSA, OPS y universidades peruanas.
    </p>
""", unsafe_allow_html=True)

# Imagen o animación simple desde una URL (compatible con Streamlit Cloud)
st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTg5cTRzM3I0dzJvZzZ2NTNjaXQ0ZTRhZTZzaHN4NjhjZ3VjY21zOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tXL4FHPSnVJ0A/giphy.gif", use_column_width=True)

# -------------------------------
# CARGA DE DATOS
# -------------------------------
with open("data/obstetricia.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# -------------------------------
# INTERFAZ INTERACTIVA
# -------------------------------
st.markdown("### 📘 Selecciona un tema y un subtema")

col1, col2 = st.columns(2)

with col1:
    tema_sel = st.selectbox("Tema", sorted(df["tema"].unique()))

with col2:
    subtemas = df[df["tema"] == tema_sel]["subtema"].unique()
    subtema_sel = st.selectbox("Subtema", subtemas)

# -------------------------------
# MOSTRAR CONTENIDO
# -------------------------------
registro = df[(df["tema"] == tema_sel) & (df["subtema"] == subtema_sel)].iloc[0]

st.markdown(f"## {registro['tema']}")
st.markdown(f"### 🩶 {registro['subtema']}")
st.write(registro["contenido"])
st.caption(f"📚 Fuente: {registro['fuente']}")

# -------------------------------
# PIE DE PÁGINA CON ANIMACIÓN GIF
# -------------------------------
st.markdown("---")
st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanIzZjdzd2l3dG1tOGc4b3A3ZDlzbm5ub3ZxZmlwdWJzY3ZxZGpzbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VbnUQpnihPSIgIXuZv/giphy.gif", width=120)
st.markdown("<p style='text-align:center;'>Desarrollado con ❤️ por <b>Justin Lavi</b><br>Datos reales del MINSA y fuentes académicas</p>", unsafe_allow_html=True)
