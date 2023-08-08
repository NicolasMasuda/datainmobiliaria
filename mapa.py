

#https://github.com/jlhonora/geo/tree/master/region_metropolitana_de_santiago
import folium
import json
import geopandas as gpd
import pandas as pd

#lo espejo falta
Lista_ubicaciones = [{"comuna":'Alhué', "ruta":"geo/alhue.geojson"},
                     {"comuna":'Buin', "ruta":"geo/buin.geojson"},
                     {"comuna":'Cerrillos',"ruta": "geo/cerrillos.geojson"},
                     {"comuna":'Cerro Navia', "ruta": "geo/cerro_navia.geojson"},
                     {"comuna":'Colina', "ruta": "geo/colina.geojson"},
                     {"comuna":'Conchalí', "ruta": "geo/conchali.geojson"},
                     {"comuna":'El Bosque', "ruta": "geo/el_bosque.geojson"},
                     {"comuna":'Estación Central', "ruta": "geo/estacion_central.geojson"},
                     {"comuna":'Huechuraba', "ruta":"geo/huechuraba.geojson"},
                     {"comuna":'Independencia', "ruta":"geo/independencia.geojson"},
                     {"comuna":'La Cisterna', "ruta":"geo/la_cisterna.geojson"}, 
                     {"comuna":'La Florida', "ruta":"geo/la_florida.geojson"},
                     {"comuna":'La Granja', "ruta":"geo/la_granja.geojson"},
                     {"comuna":'La Pintana',"ruta": "geo/la_pintana.geojson"},
                     {"comuna":'La Reina', "ruta":"geo/la_reina.geojson"},
                     {"comuna":'Lampa', "ruta":"geo/lampa.geojson"},
                     {"comuna":'Las Condes', "ruta":"geo/las_condes.geojson"},
                     {"comuna":'Lo Barnechea', "ruta":"geo/lo_barnechea.geojson"},
                     {"comuna":'Lo Prado', "ruta":"geo/lo_prado.geojson"},
                     {"comuna":'Macul', "ruta":"geo/macul.geojson"},
                     {"comuna":'Maipú', "ruta":"geo/maipu.geojson"},
                     {"comuna":'Melipilla', "ruta":"geo/melipilla.geojson"},
                     {"comuna":'Padre Hurtado', "ruta":"geo/padre_hurtado.geojson"},
                     {"comuna":'Pedro Aguirre Cerda', "ruta":"geo/pedro_aguirre_cerda.geojson"},
                     {"comuna":'Peñalolén', "ruta":"geo/penalolen.geojson"},
                     {"comuna":'Providencia', "ruta":"geo/providencia.geojson"},
                     {"comuna":'Pudahuel', "ruta":"geo/pudahuel.geojson"},
                     {"comuna":'Puente Alto', "ruta":"geo/puente_alto.geojson"},
                     {"comuna":'Quilicura', "ruta":"geo/quilicura.geojson"},
                     {"comuna":'Quinta Normal', "ruta":"geo/quinta_normal.geojson"},
                     {"comuna":'Recoleta', "ruta":"geo/recoleta.geojson"},
                     {"comuna":'Renca', "ruta":"geo/renca.geojson"},
                     {"comuna":'San Bernardo', "ruta":"geo/san_bernardo.geojson"},
                     {"comuna":'San Joaquín', "ruta":"geo/san_joaquin.geojson"},
                     {"comuna":'San Miguel', "ruta":"geo/san_miguel.geojson"},
                     {"comuna":'San Ramón', "ruta":"geo/san_ramon.geojson"},
                     {"comuna":'Santiago', "ruta":"geo/santiago.geojson"},
                     {"comuna":'Talagante', "ruta":"geo/talagante.geojson"},
                     {"comuna":'Vitacura', "ruta":"geo/vitacura.geojson"},
                     {"comuna":'Ñuñoa', "ruta":"geo/nunoa.geojson"}]

df_datos = pd.read_csv('clean_data/datos_por_ciudad.csv')
print(df_datos)

df_link = pd.read_csv('clean_data/datos_link_comuna.csv')
print(df_link)

# Iterar sobre la lista de diccionarios
for elemento in Lista_ubicaciones:
    comuna = elemento["comuna"]

    # Buscar el valor correspondiente en el DataFrame
    fila = df_datos[df_datos['cities'] == comuna]

    # Obtener los valores de "mean" y "color"
    mean_value = fila['mean'].values[0]
    color_value = fila['color'].values[0]
    count_value = fila['count'].values[0]

    # Agregar las nuevas claves al diccionario
    elemento['mean'] = mean_value
    elemento['color'] = color_value
    elemento['count'] = count_value

# Imprimir la lista de diccionarios actualizada
print(Lista_ubicaciones)


# Coordenadas de Santiago
latitud = -33.4488897
longitud = -70.6692655

# Crear el mapa centrado en Santiago
mapa_santiago = folium.Map(location=[latitud, longitud], zoom_start = 10)

for elemento in Lista_ubicaciones:
    comuna = elemento['comuna']
    ruta = elemento['ruta']
    mean = elemento['mean']
    color_comuna = elemento['color']
    count = elemento['count']

    fila = df_link[df_link['cities'] == comuna]
    print(fila)
    links_comuna = fila["link"].tolist()
    print(links_comuna)

    # Generar los elementos <a> con texto personalizado y enlace real para cada opción en links_comuna
    opciones_html = ""
    for i, link in enumerate(links_comuna):
        opcion_texto = f"Opción {i+1}"
        opciones_html += f'<a href="{link}" target="_blank">{opcion_texto}</a><br>'

    # Ruta al archivo GeoJSON
    archivo_geojson = ruta

    # Leer el archivo GeoJSON
    with open(archivo_geojson) as archivo:
        data = json.load(archivo)

    # Agregar geojson a mapa de Santiago
    folium.GeoJson(
        data,
        name="geojson",
        style_function=lambda feature, color=color_comuna: {
            'fillColor': color,
            'fillOpacity': 0.5,
            'weight': 0
        }
    ).add_to(mapa_santiago)

    # Agregar comentario
    #folium.LayerControl().add_to(mapa_santiago)

    # Leer el archivo GeoJSON
    datos_geojson = gpd.read_file(archivo_geojson)

    # Calcular el centroide del GeoJSON por comuna
    centroide = datos_geojson.geometry.centroid

    # Obtener las coordenadas del centroide por comuna
    latitud_centroide = centroide.y
    longitud_centroide = centroide.x

    # Imprimir las coordenadas del centroide OPCIONAL
    print("Latitud del centroide:", latitud_centroide[0])
    print("Longitud del centroide:", longitud_centroide[0])

    marcador = folium.Marker(
        [latitud_centroide[0], longitud_centroide[0]],
        icon=folium.Icon(color="black", icon="info-sign"),
        popup=f""" 
            <div style="text-align: center;">
                <h4>{comuna}</h4>
                <p><b>Promedio Arriendo:</b> {mean}</p>
                <p><b>Datos:</b> {count}</p>
                <p>Mejor rendimiento  m²:</p>
                {opciones_html}
            </div>""",
        tooltip="Click para más información"
    )
    marcador.add_to(mapa_santiago)

    print(comuna)
    print(ruta)

folium.LayerControl().add_to(mapa_santiago)
# Mostrar el mapa
mapa_santiago.save("mapa_final.html")
