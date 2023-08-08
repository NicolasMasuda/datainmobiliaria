import requests
import math

def obtener_categorias(url: str, lista_rutas: list) -> None:
    """
    Recupera las categorías de forma recursiva y almacena las rutas de cada categoría.

    Args:
        url (str): La URL de la API para obtener las categorías.
        lista_rutas (list): La lista para almacenar las rutas de las categorías.

    Returns:
        None

    """

    # Realizar la solicitud GET a la URL
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Obtener los datos de la respuesta
    ruta = data["path_from_root"]
    categorias = data["children_categories"]

    # Imprimir información de depuración
    #print(ruta)
    #print(len(categorias))
    #print("**************************************")

    # Verificar si no hay categorías hijas
    if len(categorias) == 0:
        lista_rutas.append(ruta)  # Agregar la ruta a la lista
        #print("PERFECTO ES 00000000000000000000000000000000")
    else:
        pass
        #print(" MAL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    #print("**************************************")

    # Recorrer las categorías hijas de forma recursiva
    for categoria in categorias:
        id = categoria["id"]
        categoria_1 = categoria["name"]
        data_categoria = categoria["total_items_in_this_category"]
        #print("---ID: " + str(categoria["id"]))
        #print("---NAME: " + str(categoria["name"]))
        #print("---Total Data: " + str(categoria["total_items_in_this_category"]))
        url_categoria = f"https://api.mercadolibre.com/categories/{id}"
        #print(f"""La url es: {url_categoria}""")
        #print("**************************************")

        # Llamar a la función de forma recursiva con la categoría hija
        obtener_categorias(url_categoria, lista_rutas)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def crear_diccionarios_categorias(lista_rutas: list) -> list:
    """
    Crea una lista de diccionarios que representan las categorías de productos.
    
    Cada diccionario contiene las siguientes claves:
    - id_categoria: ID de la categoría para la URL.
    - categoria_1: Categoría principal.
    - categoria_2: Categoría secundaria.
    - categoria_3: Tipo de oferta.

    Args:
        lista_rutas (list): Lista de rutas de categorías.

    Returns:
        list: Lista de diccionarios con la información de las categorías.
    """

    lista_diccionarios = []

    for ruta in lista_rutas:
        if len(ruta) == 4:
            diccionario = {
                "id_categoria": ruta[-1]["id"],
                "categoria_1": ruta[-3]["name"],
                "categoria_2": ruta[-2]["name"],
                "categoria_3": ruta[-1]["name"]
            }
        elif len(ruta) == 3:
            diccionario = {
                "id_categoria": ruta[-1]["id"],
                "categoria_1": ruta[-3]["name"],
                "categoria_2": ruta[-2]["name"],
                "categoria_3": ruta[-1]["name"]
            }
        else:
            continue

        lista_diccionarios.append(diccionario)

    return lista_diccionarios

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def filtro_categoria(lista_categorias: list, categoria_1: str) -> list:
    """
    Filtra una lista de categorías por el valor de la clave 'categoria_1'.

    Args:
        lista_categorias (list): Lista de diccionarios con las categorías.
        categoria_1 (str): Valor de la clave 'categoria_1' para filtrar.

    Returns:
        list: Lista de diccionarios que coinciden con la categoría filtrada.
    """
    resultados = []

    # Iterar sobre cada categoría en la lista
    for categoria in lista_categorias:
        # Comprobar si la categoría coincide con la categoría filtrada
        if categoria["categoria_1"] == categoria_1:
            resultados.append(categoria)

    return resultados

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#


def obtener_region() -> list:
    """
    Obtiene una lista de las regiones de Chile utilizando la API de MercadoLibre.

    Returns:
        list: Lista de diccionarios con los valores "id" y "name" de cada región.

    Raises:
        Exception: Si ocurre un error al obtener los datos.
    """

    # URL de la API que contiene las regiones de Chile
    url = "https://api.mercadolibre.com/classified_locations/countries/CL"

    try:
        # Realizar solicitud GET a la URL
        response = requests.get(url)

        # Verificar el código de respuesta
        response.raise_for_status()

        # Extraer los datos de la respuesta en formato JSON
        data = response.json()

        # Obtener la lista de regiones del objeto "states"
        regiones = data["states"]

        # Crear una lista de diccionarios para almacenar los pares "id" y "name"
        resultados = []

        # Recorrer cada región y obtener los valores "id" y "name"
        for region in regiones:
            region_id       = region["id"]
            nombre_region   = region["name"]

            # Agregar los valores a la lista de resultados
            resultados.append({"id": region_id, "name": nombre_region})

        # Retornar la lista con los valores "id" y "name"
        return resultados

    except requests.exceptions.RequestException as e:
        # Si ocurre un error durante la solicitud, levantar una excepción
        raise Exception(f"Error al obtener los datos: {str(e)}")

    except (KeyError, ValueError) as e:
        # Si ocurre un error al procesar los datos, levantar una excepción
        raise Exception("Error al procesar los datos de la API")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def obtener_region_ciudad() -> list:
    """
    Obtiene una lista de regiones y ciudades de Chile utilizando la API de MercadoLibre.

    Esta función depende de la función `obtener_region()` para obtener la lista de regiones.

    Returns:
        list: Lista de diccionarios con los valores "id", "name" y "cities" de cada región.

    Raises:
        Exception: Si ocurre un error al obtener los datos.
    """

    # Obtener la lista de regiones
    lista_region = obtener_region()

    resultados = []

    # Recorrer la lista de regiones
    for region in lista_region:
        region_id   = region["id"]
        region_name = region["name"]

        # Construir la URL de la API para obtener las ciudades de la región
        url = f"https://api.mercadolibre.com/states/{region_id}"

        try:
            # Realizar solicitud GET a la URL
            response = requests.get(url)

            # Verificar el código de respuesta
            response.raise_for_status()

            # Obtener los datos de la región en formato JSON
            data = response.json()

            # Verificar si la clave "cities" existe en los datos de respuesta
            if "cities" in data:
                ciudades = data["cities"]

                # Agregar la región y las ciudades a la lista de resultados
                resultados.append({"id": region_id, "name": region_name, "cities": ciudades})

            else:
                raise KeyError("No se encontró la clave 'cities' en los datos de respuesta.")

        except requests.exceptions.RequestException as e:
            # Si ocurre un error durante la solicitud, levantar una excepción
            raise Exception(f"Error al obtener los datos: {str(e)}")

        except (KeyError, ValueError) as e:
            # Si ocurre un error al procesar los datos, levantar una excepción
            raise Exception("Error al procesar los datos de la API")

    return resultados


def filtro_region(lista_ubicaciones: list, region: str )-> list:
    resultados = []

    # Iterar sobre cada categoría en la lista
    for ubicacion in lista_ubicaciones:
        # Comprobar si la categoría coincide con la categoría filtrada
        if ubicacion["name"] == region:
            resultados.append(ubicacion)

    return resultados

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#


def informacion_categoria_region_ciudad_url(lista_categorias: list, lista_ubicaciones: list) -> list:
    """
    Genera una lista de información de categoría, región, ciudad y URL para realizar búsquedas.

    Args:
        lista_categorias (list): Lista de diccionarios con las categorías.
        lista_ubicaciones (list): Lista de diccionarios con las ubicaciones.

    Returns:
        list: Lista de diccionarios con la información de categoría, región, ciudad y URL.
    """
    resultados = []
    id = 0
    url_base = "https://api.mercadolibre.com/sites/MLC/search?category="

    # Iterar sobre cada diccionario de categoría
    for diccionario in lista_categorias:
        categoria = diccionario['id_categoria']
        categoria_1 = diccionario['categoria_1']
        categoria_2 = diccionario['categoria_2']
        categoria_3 = diccionario['categoria_3']
        url_categoria = f"{url_base}{categoria}"

        # Iterar sobre cada diccionario de ubicación
        for region in lista_ubicaciones:
            region_id = region['id']
            region_name = region['name']
            ciudades = region['cities']

            # Iterar sobre cada diccionario de ciudad dentro de la región
            for ciudad in ciudades:
                lugar_id = ciudad['id']
                lugar_name = ciudad["name"]
                url = f"{url_categoria}&state={region_id}&city={lugar_id}"

                # Agregar la información a la lista de resultados
                resultados.append({"id": id, "region": region_name, "city": lugar_name, "url": url, "categoria_1": categoria_1, "categoria_2": categoria_2, "categoria_3": categoria_3})
                id += 1

    return resultados

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
 
def datos_inmobilario(datos_url:list):
    """
    Extrae datos inmobiliarios de una lista de URLs y los devuelve en una lista de diccionarios.
    Cada diccionario contiene información sobre una propiedad inmobiliaria.

    Args:
        datos_url (list): Lista de diccionarios que contienen información sobre las URL de consulta.

    Returns:
        list: Lista de diccionarios con la información inmobiliaria extraída.
    """
    id = 0
    informacion = []
    cont = 0
    for datos in datos_url:
        url = datos["url"]
        #print(url)
        region = datos["region"]
        city = datos["city"]
        response = requests.get(url)
        data = response.json()

        numero_datos = int(data["paging"]["total"])
    
        if numero_datos == 0:
            pass

        if numero_datos <= 50:
            data_results = data["results"]
            for results in data_results:

                id_item     = results['id']
                precio      = results['price']
                moneda      = results['currency_id']
                titulo      = results['title']
                link        = results['permalink']
                lugar       = results["location"]["address_line"]
                atributos   = results["attributes"]

                for atributo in atributos:

                    if atributo["id"] == "BEDROOMS":
                        dormitorios = atributo["value_name"]

                    if atributo["id"] == "COVERED_AREA":
                        superficie_util = atributo["value_name"]

                    if atributo["id"] == "FULL_BATHROOMS":
                        banos = atributo["value_name"]

                    if atributo["id"] == "TOTAL_AREA":
                        superficie_total = atributo["value_name"]
                # Verificar si el atributo "COVERED_AREA" existe
                if "superficie_util" not in locals():
                    superficie_util = "N/A"

                id = id + 1
                informacion.append({"id": id,
                                    "region": region,
                                    "cities": city,
                                    "id_item": id_item,
                                    "categoria_1": datos["categoria_1"],
                                    "categoria_2": datos["categoria_2"],
                                    "categoria_3": datos["categoria_3"],
                                    "precio": precio,
                                    "moneda": moneda,
                                    "titulo": titulo,
                                    "link": link,
                                    "lugar": lugar,
                                    "dormitorios": dormitorios,
                                    "superficie_util": superficie_util,
                                    "banos": banos,
                                    "superficie_total": superficie_total,

                                    })

        if numero_datos > 50:
            ratio = numero_datos/50
            redondeado = math.ceil(ratio)
            for i in range(redondeado):
                inicio = 50 * i

                if inicio <= 950:
                    #print(inicio)
                    #print(f"{url}&offset={inicio}&limit=50")
                    url_datos = f"{url}&offset={inicio}&limit=50"
                    response = requests.get(url_datos)
                    data = response.json()
                    data_results = data["results"]
                    for results in data_results:

                        id_item     = results['id']
                        precio      = results['price']
                        moneda      = results['currency_id']
                        titulo      = results['title']
                        link        = results['permalink']
                        lugar       = results["location"]["address_line"]
                        atributos   = results["attributes"]

                        for atributo in atributos:
                            if atributo["id"] == "BEDROOMS":
                                dormitorios = atributo["value_name"]

                            if atributo["id"] == "COVERED_AREA":
                                superficie_util = atributo["value_name"]

                            if atributo["id"] == "FULL_BATHROOMS":
                                banos = atributo["value_name"]

                            if atributo["id"] == "TOTAL_AREA":
                                superficie_total = atributo["value_name"]
                                
                        # Verificar si el atributo "COVERED_AREA" existe
                        if "superficie_util" not in locals():
                            superficie_util = "N/A"

                        id = id + 1
                        informacion.append({"id": id,
                                            "region": region,
                                            "cities": city,
                                            "id_item": id_item,
                                            "categoria_1": datos["categoria_1"],
                                            "categoria_2": datos["categoria_2"],
                                            "categoria_3": datos["categoria_3"],
                                            "precio": precio,
                                            "moneda": moneda,
                                            "titulo": titulo,
                                            "link": link,
                                            "lugar": lugar,
                                            "dormitorios": dormitorios,
                                            "superficie_util": superficie_util,
                                            "banos": banos,
                                            "superficie_total": superficie_total,
                                            })
                
                else:
                    pass
        
        print(f"""
        ***************************
        Progreso: {cont}/{len(datos_url)}
        ***************************
        """)
        cont = cont + 1

    return informacion

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# #https://api.mercadolibre.com/sites/MLC/search?category=MLC183186&offset=0&limit=50
# #https://developers.mercadolibre.cl/devcenter
# #https://developers.mercadolibre.com.mx/en_us/en_us/items-and-searches
# #https://www.youtube.com/watch?v=i9IezaDb2cM&ab_channel=miguelsanchezco #VERRRRR
# #https://api.mercadolibre.com/states/TUxDUE1FVEExM2JlYg