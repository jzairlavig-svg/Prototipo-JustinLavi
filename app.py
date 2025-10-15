import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="Apuntes de Obstetricia",
    page_icon="👩‍⚕️",
    layout="wide",
)

# --- CSS simple para animaciones y estilo ---
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    font-family: 'Arial', sans-serif;
}

.title {
    text-align: center;
    font-size: 42px;
    color: #2c3e50;
    animation: fadeInDown 1s ease;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #7f8c8d;
    margin-bottom: 40px;
    animation: fadeIn 2s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.card {
    background-color: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
}

.footer {
    text-align: center;
    font-size: 14px;
    color: #95a5a6;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado principal ---
st.markdown("<h1 class='title'>👩‍⚕️ Apuntes de Obstetricia</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Resumen de temas clave con datos reales y fuentes confiables</p>", unsafe_allow_html=True)

# --- Datos reales ---
datos = [
    {
        "tema": "Definición de obstetricia",
        "subtema": "Concepto general",
        "contenido": "La obstetricia es la rama de la medicina que trata de la gestación, el parto y el puerperio.",
        "fuente": "RAE"
    },
    {
        "tema": "Nutrición en el embarazo",
        "subtema": "Sobrepeso gestacional",
        "contenido": "Entre 2009 y 2019, la prevalencia de sobrepeso en gestantes en Perú pasó de 30.4 % a 44 %. Esto incluye gestantes que empezaron el embarazo con sobrepeso (33.6 %) u obesidad (13.5 %).",
        "fuente": "Ministerio de Salud / INS, reporte SIEN 2020"
    },
    {
        "tema": "Mortalidad materna",
        "subtema": "Cifras recientes",
        "contenido": "En 2021 se reportaron 493 muertes maternas en Perú. Las causas más comunes fueron hemorragia obstétrica, trastornos hipertensivos del embarazo, parto y puerperio. En 2023-2024 la tasa de mortalidad neonatal fue de aproximadamente 7 muertes por cada 1000 nacidos vivos.",
        "fuente": "MINSA / CDC Perú / Mesa de Concertación"
    },
    {
        "tema": "Control prenatal",
        "subtema": "Importancia del seguimiento",
        "contenido": "El control prenatal temprano permite detectar factores de riesgo y reducir complicaciones durante el embarazo. En Perú, el 89.7 % de las gestantes recibió al menos un control prenatal en 2023.",
        "fuente": "INEI, Encuesta Demográfica y de Salud Familiar (ENDES) 2023"
    },
    {
        "tema": "Parto institucional",
        "subtema": "Acceso y cobertura",
        "contenido": "El 95.3 % de los partos en Perú en 2023 fueron atendidos en establecimientos de salud, mejorando la cobertura respecto al 91.6 % en 2015.",
        "fuente": "INEI, ENDES 2023"
    }
]

# --- Mostrar datos como “tarjetas” ---
for item in datos:
    st.markdown(f"""
    <div class='card'>
        <h3>📘 {item['tema']}</h3>
        <h5 style='color:#2980b9;'>{item['subtema']}</h5>
        <p style='font-size:16px;'>{item['contenido']}</p>
        <p style='font-size:13px; color:#7f8c8d;'><b>Fuente:</b> {item['fuente']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- Pie de página ---
st.markdown("<p class='footer'>Creado con ❤️ por Justin Lavi | Datos: MINSA, INS, INEI</p>", unsafe_allow_html=True)
