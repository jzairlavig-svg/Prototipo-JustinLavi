import streamlit as st
import json
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# --- Configuración inicial ---
st.set_page_config(page_title="Apuntes de Obstetricia", page_icon="🩺", layout="centered")

# --- Función para cargar animaciones Lottie ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Animación de portada ---
lottie_header = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_h4th9ofg.json")  # animación médica

# --- Título principal ---
st.title("🩺 Apuntes de Obstetricia")
st.markdown("### Material de referencia real basado en datos del MINSA, OPS y universidades peruanas")

# --- Mostrar animación ---
st_lottie(lottie_header, height=200, key="header")

# --- Cargar datos desde JSO
