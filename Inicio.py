import streamlit as st
from constants import constant as const

st.set_page_config(
    page_title="Inicio",
    layout="centered",
    page_icon="static/logo-crea.png",
)

st.markdown(const.oculta_deploy, unsafe_allow_html=True)

st.write("# Bienvenido al Monitor Forrajero 👋")
st.markdown(
    """
    Esta es una sencilla aplicación que sirve de ayuda para la digitalización de lotes.
    
    La pestaña Consultar permite ver los lotes de un grupo que han sufrido modificaciones
    en sus ocupaciones para un rango de fechas determinado.
    
    Por su parte la pestaña exportar permite ver los lotes de los campos de un determinado grupo.
    Se pueden ver todos los lotes o solo los activos **tildando/destildando** el check **Todos los lotes del grupo**.
    En la misma pestaña se puede exportar un zip que contiene todos los archivos shapefile.
"""
)