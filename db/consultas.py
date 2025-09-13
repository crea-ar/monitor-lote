import pandas as pd
import db.base as base

def grupos_por_fecha(params:None):
  query = f"""
          SELECT grupo_region as GRUPO,
            campo as CAMPO,
            lote as LOTE,
            ocupacion_fecha_modificacion as 'FECHA MODIFICACION'
          FROM v_consulta_lotes_modificados 
          WHERE ocupacion_fecha_modificacion >= %s AND ocupacion_fecha_modificacion <= %s
      """
  df = base.consulta_base(query, params)
  return df

def grupos_select():
  query = f"SELECT DISTINCT grupo_region FROM v_shape_file ORDER BY grupo_region"
  df = base.consulta_base(query, None)
  return df['grupo_region'].dropna().tolist()

def datos_por_grupo(grupo, todos):
	query = f"""SELECT grupo as GRUPO,
					campo as CAMPO,
					lote as LOTE,
					uso as USO,
					fecha_desde as DESDE,
					fecha_hasta as HASTA,
					lote_geo
					FROM v_shape_file WHERE grupo_region = %s"""
	if not todos:		
		query += " and fecha_desde <= now() and (fecha_hasta > now() or fecha_hasta is null)"
  
	df = base.consulta_base(query, params=(grupo,))
	return df
