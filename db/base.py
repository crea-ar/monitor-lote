import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def conexion():
  try:
    env_path = 'db/credenciales.env'
    load_dotenv(env_path)

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

  except Exception as e:
    raise Exception(f"Error al conectar a la base de datos: {str(e)}")


def consulta_base(query, params:None):
  try:
    con = conexion()
    df = pd.read_sql(query, con, params=params)
    return df
  except Exception as e:
    raise Exception(f"Error al consultar la base: {str(e)}")
