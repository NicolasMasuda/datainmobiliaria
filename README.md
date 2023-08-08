# Proyecto de Datos Inmobiliarios de Gran Santiago

Este proyecto utiliza la API de Mercado Libre para recopilar y analizar datos inmobiliarios de la región de Gran Santiago, Chile. El objetivo principal es obtener información sobre propiedades en venta y calcular métricas relevantes para el mercado inmobiliario.

## Descripción del Proyecto

El proyecto consta de varias etapas, cada una con su propio script:

1. **API.py**: Este script recopila información de las categorías y ubicaciones utilizando la API de Mercado Libre. Las funciones incluyen:

    - `obtener_categorias(url, lista_rutas)`: Recopila las categorías de forma recursiva y almacena las rutas.
    - `crear_diccionarios_categorias(lista_rutas)`: Crea una lista de diccionarios que representan las categorías.
    - `filtro_categoria(lista_categorias, categoria_1)`: Filtra las categorías por la categoría principal.
    - `obtener_region()`: Obtiene una lista de las regiones de Chile.
    - `obtener_region_ciudad()`: Obtiene una lista de regiones y ciudades de Chile.
    - `filtro_region(lista_ubicaciones, region)`: Filtra las ubicaciones por región.
    - `informacion_categoria_region_ciudad_url(lista_categorias, lista_ubicaciones)`: Genera una lista de información de categoría, región, ciudad y URL.

2. **data_create.py**: Utiliza las funciones de `API.py` para crear dos archivos .json con datos crudos que se almacenan en la carpeta `DATA`. El script realiza las siguientes acciones:
   - Importa el módulo `API` que contiene funciones para obtener categorías, ubicaciones y datos inmobiliarios.
   - Define una función `convertir_lista_a_txt(lista, nombre_archivo, carpeta)` para convertir una lista de diccionarios en un archivo .txt.
   - Define una función `crear_datos_filtro(url, categoria, region)` que utiliza las funciones de `API.py` para filtrar categorías y ubicaciones, y luego recopila datos inmobiliarios en función de los filtros.
   - Calcula y muestra el tiempo transcurrido para ejecutar el proceso.

3. **lectura.py**: Limpia los datos crudos y almacena los datos limpios en la carpeta `clean_data`.

	- `remover_m2(df, superficie: str)`: Remueve la unidad "m²" de una columna de superficie en un DataFrame.
	- `convertir_precio_CLP(row, cambio_CLF, cambio_USD)`: Convierte el precio a CLP utilizando tasas de cambio proporcionadas.
	- `metro_precio(row, superficie)`: Calcula el precio por metro cuadrado.
	- `eliminar_outliers_por_ciudad(df, columna, umbral)`: Elimina los outliers de una columna por ciudad.
	- `obtener_minimos(group)`: Obtiene las 5 filas con el valor mínimo de la columna "precio_metro_util".

### Procesamiento de Datos

	- Lectura del archivo JSON con datos inmobiliarios.
	- Conversión de las columnas de superficie a números.
	- Conversión de precios a CLP.
	- Eliminación de filas con superficie total y utilidad igual a cero.
	- Asignación de valor de utilidad a superficie total igual a cero.
	- Cálculo de precio por metro cuadrado para superficie total y utilidad.

### Análisis de Datos

	- Filtrado de propiedades de arriendo y propiedades usadas.
	- Eliminación de outliers por ciudad en precio y superficie.
	- Cálculo de la media y cantidad de propiedades por ciudad.
	- Obtención de las 5 propiedades con menor precio por metro cuadrado por ciudad.
	- Creación de archivo CSV con los resultados.

### Uso

1. Ejecuta el script `lectura.py` después de haber ejecutado `data_create.py`.
2. El script realizará la limpieza y análisis de los datos obtenidos.
3. Los resultados se guardarán en archivos CSV en la carpeta `clean_data`.

4. **mapa.py**: Crea un mapa de calor interactivo en HTML con los inmuebles más eficientes en términos de precio/metro cuadrado.

Este script utiliza la biblioteca Folium para generar un mapa interactivo que muestra los datos inmobiliarios analizados en el proyecto de Datos Inmobiliarios de Gran Santiago.

### Uso

1. Asegúrate de ejecutar previamente los scripts `data_create.py` y `lectura.py`.
2. Ejecuta este script `mapa_inmobiliario.py` después de haber creado y procesado los datos.
3. El mapa generado se guardará como un archivo HTML llamado "mapa_final.html" en el mismo directorio.

## Cómo Utilizar

1. Ejecuta `API.py` para obtener datos de categorías y ubicaciones de Mercado Libre.
2. Ejecuta `data_create.py` para generar archivos .json con datos crudos.
3. Ejecuta `lectura.py` para limpiar los datos y guardarlos en la carpeta `clean_data`.
4. Ejecuta `mapa.py` para generar un mapa de calor interactivo con los datos limpios.

## Requisitos

- Python 3.x
- - Bibliotecas: folium, json, geopandas, pandas

## Contribuciones

Siéntete libre de contribuir al proyecto creando solicitudes pull o informando problemas en el repositorio.


## Autor

[Nicolás Masuda]
