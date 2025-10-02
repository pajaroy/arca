#!/bin/bash
# ~/@arca/source/main.py
# Version: 0.1.0
# Descripcion: Script para clasificar archivos por formato
#  - Extrae archivos de cualquier carpeta
#  - Calcula el hash con blake3
#  - Verifica los hash en destino para evitar colisiones
#  - Revisa con fdupes (o alguna alternativa para evitar duplicados textuales)
#  - Genera logs de cada archivo
# Flujo de trabajo:
#  - Toma los archivos desde /data/raw
#  - Los clasifica por formato
#  - Calcula el hash con blake3 
#  - Deposita los archivos en /data/staging
#  - Inicia la base de datos csv
#  - indexa todo en /data/staging/database.csv (alegoria a la data basica recien ordenada)
#  
# Reglas de oro:
#  - Todo debe poder ser exportado para luego ir extendiendolo para cargar todo a sql.
# 
# Estructura del script:
#  - load_config: Carga la configuracion base 
#  - Funciones principales: ver indice mas abajo
# 
# 
#
#
#################################################################################################################

import os
import blake3
import shutil

#################################################################################################################
# Definiciones base:
# Esto podriamos definirlo en la config.yaml de la raiz de /data/config.yaml
#
root="~/@arca"
#
# root_data="~/@arca/data" esta parte la deje comentada por qe no estoy seguro de como iria
#
formato=["csv","markdown","otros","python","sql","yaml"] # podria ir en config.yaml si no complejiza mucho
#
metadata=["ruta","nombre","tipo","tamano_bytes","fecha_mod","palabras_clave","hash_blake3","contenido","palabras_limpias"]
#
root_log=~/@arca/datalogs/datalogs.csv"
#################################################################################################################

# Cargar config.yaml

class load_config():

# Deberia cargar la config desde root.data.config.yaml


# Crear directorios si no existe:

for dir in formato:

    root_dir=os.path.join(root_source,dir)

    if not os.path.exists

#################################################################################################################
# Funciones principales:
#  - classifier: clasifica los archivos por formato
#  - calc_hash: Calcula el hash de los archivos
#  - hash_integridad: Revisa los hash en la base de datos para no sobreescribir nada
#  - init_database: Prepara la base de datos para recibir nuevos datos, siempre agregando sobre la misma base
#  - logger: logea en la ruta de los logs
#################################################################################################################

# Clase para extraer y clasificar archivos :

class classifier():

# Hashing e indexado

class calc_hash():

# Verifica los hashes en la carpeta de destino para no repetir hash
# Esta funcion la utilizaremos para comparar los archivos con la base de datos

class hash_integridad():


# database: Aca armaremos una base de datos .csv en /data/processed/database.csv
# Esto podriamos hacerlo todo en una sola funcion qe inicie la db y que cargue todo en csv

class init_database():


# logger qe logeara en /data/logs/logs.csv

class logger():

# deberia ir un logger generico qe loguee siempre aca todo lo generado dentro de data


#################################################################################################################
# Main:
# El main deberia correr todo el ciclo de una para correr python3 ~/@arca/data/main.py y quede todo echo y clasificado lo qe hayamos agregado
#################################################################################################################

def main():


