import pandas as pd
import streamlit as st

st.title("Eventos de alarma")

df = pd.read_csv("data/eventos_alarma.csv")
provincia = st.selectbox("Provincia", sorted(df["provincia"].unique()))

filtrado = df[df["provincia"] == provincia]

_, col_centro, _ = st.columns([1, 2, 1])
with col_centro:
    st.metric("Eventos", len(filtrado))
st.dataframe(filtrado.head(50))
