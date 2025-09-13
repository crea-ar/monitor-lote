import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
from sqlalchemy import create_engine
import os
import zipfile
import shutil
from constants import constant as const
import db.consultas as consultas

def exportar_shapefile(df, nombre_archivo_base="lotes_exportados"):
	df['geometry'] = df['lote_geo'].apply(wkt.loads)

	gdf = gpd.GeoDataFrame(df, geometry='geometry')
	gdf.set_crs(epsg=3857, inplace=True)  # Proyección original
	gdf = gdf.to_crs(epsg=4326)           # Reproyectamos a EPSG:4326

	# Eliminamos la columna lote_geo (WKT) para no incluirla en el DBF
	if 'lote_geo' in gdf.columns:
		gdf = gdf.drop(columns=['lote_geo'])

	# Carpeta temporal
	output_dir = "temp_shape"
	os.makedirs(output_dir, exist_ok=True)

	# Paths
	shp_base_path = os.path.join(output_dir, nombre_archivo_base)
	shp_path = f"{shp_base_path}.shp"

	# Guardar shapefile
	gdf.to_file(shp_path)

	# Crear ZIP dentro de la misma carpeta
	zip_filename = f"{nombre_archivo_base}.zip"
	zip_full_path = os.path.join(output_dir, zip_filename)

	with zipfile.ZipFile(zip_full_path, 'w') as zipf:
		for ext in ['shp', 'shx', 'dbf', 'prj', 'cpg']:
			file = f"{shp_base_path}.{ext}"
			if os.path.exists(file):
				zipf.write(file, arcname=os.path.basename(file))

	# Limpieza de archivos temporales (solo los del shapefile)
	for ext in ['shp', 'shx', 'dbf', 'prj', 'cpg']:
		file = f"{shp_base_path}.{ext}"
		if os.path.exists(file):
			os.remove(file)

	return zip_full_path, zip_filename


# ---------------------------
# INTERFAZ DE STREAMLIT
# ---------------------------

st.set_page_config(
  page_title="Exportar",
  layout="wide",
  initial_sidebar_state="expanded",
)

st.markdown(const.oculta_deploy, unsafe_allow_html=True)
st.title("Lotes por Grupo CREA")

# Selección del grupo
#grupos = get_grupos()
grupos = consultas.grupos_select()
grupo_seleccionado = st.selectbox("Seleccioná un grupo:", grupos, width=600)

# Checkbox para seleccionar "Todos los lotes del grupo" o "Solo lotes activos"
todos_lotes = st.checkbox("Todos los lotes del grupo", value=False)

# Cambiar el label del checkbox dependiendo de su estado
if todos_lotes:
  st.write("Mostrando **todos los lotes** del grupo.") 
else:
  st.write("Mostrando **solo los lotes activos** del grupo.") 
    
#Consultar en base a la opción seleccionada
if grupo_seleccionado:
	df = consultas.datos_por_grupo(grupo_seleccionado, True) if todos_lotes else consultas.datos_por_grupo(grupo_seleccionado, False)

	# # Ejecutamos la consulta
	# df = pd.read_sql(query, engine, params=(grupo_seleccionado,))

	# Mostramos los resultados
	#st.write(f"Total de registros encontrados: {len(df)}")
	st.success(f"{len(df)} registros encontrados.")
 
	st.dataframe(df, width="content")

	# 4. Botón para exportar a shapefile
	if st.button("📦 Exportar a Shapefile"):
		with st.spinner("Generando archivos..."):
			nombre_base = 'CREA_' + df.loc[1, 'GRUPO'].replace(" ", "")
			#nombre_base = f"{grupo_seleccionado.replace(' ', '_')}"
			zip_file_path, zip_file_name = exportar_shapefile(df, nombre_base)

			# Descargar el archivo ZIP
			with open(zip_file_path, "rb") as f:
				st.download_button(
					label="⬇️ Descargar Shapefile (ZIP)",
					data=f,
					file_name=zip_file_name,
					mime="application/zip"
				)

			# Limpiar archivos temporales (solo el ZIP, sin borrar la carpeta)
			if os.path.exists(zip_file_path):
				os.remove(zip_file_path)
