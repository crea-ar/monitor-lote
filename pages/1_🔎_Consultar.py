import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from constants import constant as const
import db.consultas as consultas

# ---------------------------
# INTERFAZ STREAMLIT
# ---------------------------

st.set_page_config(
  page_title="Consultar",
  layout="wide",
  initial_sidebar_state="expanded",
)

st.markdown(const.oculta_deploy, unsafe_allow_html=True)
st.title("Lotes con ocupaciones modificadas")

# Selectores de fecha
columna1, columna2, columna3 = st.columns(3, gap="small")

with columna1:
  fecha_desde = st.date_input("📅 Fecha Desde", width=300, format="DD/MM/YYYY")
with columna2:
  fecha_hasta = st.date_input("📅 Fecha Hasta", width=300, format="DD/MM/YYYY")

#Validar fechas
if fecha_desde > fecha_hasta:
  st.error("La fecha 'Desde' no puede ser posterior a la fecha 'Hasta'.")
else:
  if st.button("🔍 Consultar"):
    with st.spinner("Consultando base de datos..."):
      df =  consultas.grupos_por_fecha((fecha_desde, fecha_hasta)) 
      st.success(f"{len(df)} registros encontrados.")
      st.dataframe(df, width="stretch")
      
      
