"""Panel de eventos de alarma · punto de partida del laboratorio.

Datos SINTÉTICOS generados con generar_datos.py.
Ejecutar:  streamlit run app.py
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Eventos de alarma", layout="wide")
st.title("Eventos de alarma")
st.caption("Datos sintéticos para formación")

# PASO 7 del laboratorio: mueve esta carga a una función con @st.cache_data
df = pd.read_csv("data/eventos_alarma.csv", parse_dates=["fecha_hora"])

with st.sidebar:
    st.header("Filtros")
    provincias = st.multiselect("Provincia", sorted(df["provincia"].unique()))
    tipos = st.multiselect("Tipo de evento", sorted(df["tipo_evento"].unique()))
    # PASO 3: añade aquí un filtro de fechas con st.date_input

filtrado = df.copy()
if provincias:
    filtrado = filtrado[filtrado["provincia"].isin(provincias)]
if tipos:
    filtrado = filtrado[filtrado["tipo_evento"].isin(tipos)]

# PASO 4: sustituye esta métrica por una fila de tres con st.columns(3)
st.metric("Eventos", f"{len(filtrado):,}".replace(",", "."))

# PASO 5: crea pestañas con st.tabs y añade la evolución mensual por tipo
st.subheader("Eventos por provincia")
st.bar_chart(filtrado["provincia"].value_counts())

st.subheader("Detalle")
st.dataframe(filtrado.head(200), width="stretch")

# PASO 6: añade un st.download_button para descargar `filtrado` en CSV
