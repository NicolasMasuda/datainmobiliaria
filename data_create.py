import API
import time
from datetime import timedelta
import datetime
import requests
import math
import os
import json

def convertir_lista_a_txt(lista, nombre_archivo, carpeta):
    ruta_archivo = os.path.join(carpeta, nombre_archivo)

    with open(ruta_archivo, 'w') as archivo:
        archivo.write("[")  # Escribir corchete de apertura al principio del archivo

        for i, elemento in enumerate(lista):
            cadena = json.dumps(elemento)  # Convertir el diccionario en una cadena de texto JSON
            archivo.write(cadena)  # Escribir la cadena JSON en el archivo

            if i < len(lista) - 1:
                archivo.write(",")  # Agregar coma al final de cada cadena, excepto la última
            
            archivo.write('\n')
        
        archivo.write("]")  # Escribir corchete de cierre al final del archivo

    print(f"Se ha creado el archivo {nombre_archivo} en la carpeta {carpeta} con éxito.")


def crear_datos_filtro(url,categoria, region):
    lista_rutas = []  # Crear una lista vacía para almacenar las rutas
    API.obtener_categorias(url, lista_rutas)
    #print(lista_rutas)  # Imprimir la lista de rutas

    lista_categorias = API.crear_diccionarios_categorias(lista_rutas)
    # Imprimir la lista de diccionarios
    API.filtro_categoria(lista_categorias,categoria)
    lista_categoria_casas = API.filtro_categoria(lista_categorias,categoria)

    lista_ubicaciones = API.obtener_region_ciudad()
    #print(lista_ubicaciones)

    #print("********************************")
    #for ubicaciones in lista_ubicaciones:
    #    print(ubicaciones)

    Lista_ubicaciones_filtro = API.filtro_region(lista_ubicaciones, region)
    print(Lista_ubicaciones_filtro)

    datos_url = API.informacion_categoria_region_ciudad_url(lista_categoria_casas,Lista_ubicaciones_filtro)
    print(datos_url)
    print(len(datos_url))

    datos_bruto = API.datos_inmobilario(datos_url)
    fecha_actual = datetime.date.today()

    convertir_lista_a_txt(datos_bruto, f"data_{categoria}_{region}_{fecha_actual}.json", "DATA")

#Inicia temporizador 
inicio = time.time()


url = "https://api.mercadolibre.com/categories/MLC1459"
categoria = 'Departamentos'
region = "RM (Metropolitana)"
crear_datos_filtro(url,categoria, region)



#------------------TIEMPO------------------#

# Calcular el tiempo transcurrido
tiempo_transcurrido = time.time() - inicio

# Convertir el tiempo transcurrido a un objeto timedelta
tiempo_delta = timedelta(seconds = tiempo_transcurrido)

# Obtener la representación legible del tiempo
tiempo_legible = str(tiempo_delta)

# Imprimir el tiempo legible
print(f"""
****************************************************
****************************************************
Tiempo transcurrido: {tiempo_legible}
****************************************************
****************************************************
""")