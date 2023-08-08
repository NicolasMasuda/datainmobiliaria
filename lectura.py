import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap


#----------------------Funciones-------------#
#'superficie_total' , 'superficie_util'
def remover_m2 (df, superficie: str):

    df[superficie] = df[superficie].astype(str).str.replace(' m²', '')

    #Transformar superficie_total en float para trabajar
    df[superficie] = df[superficie].astype(float)
    return df

#-------------------------------------------
#-----------------------
def convertir_precio_CLP(row,cambio_CLF, cambio_USD):
    if row['moneda'] == 'CLF':
        return row['precio'] * cambio_CLF
    elif row['moneda'] == 'USD':
        return row['precio'] * cambio_USD
    else:
        return row['precio']

#-------------------------------------------
#-----------------------
def metro_precio(row,superficie):
    return row["precio_CLP"]/row[superficie]


def eliminar_outliers_por_ciudad(df, columna, umbral):
    grupos = df.groupby('cities')
    df_filtrado = pd.DataFrame()
    
    for ciudad, grupo in grupos:
        media = grupo[columna].mean()
        desviacion_estandar = grupo[columna].std()
        grupo_filtrado = grupo[(grupo[columna] > media - umbral * desviacion_estandar) & (grupo[columna] < media + umbral * desviacion_estandar)]
        df_filtrado = pd.concat([df_filtrado, grupo_filtrado])
    
    return df_filtrado

# Definir la función para obtener las 5 filas con el valor mínimo de la columna "precio_metro_util"
def obtener_minimos(group):
    return group.nsmallest(5, 'precio_metro_util')


# Ruta del archivo JSON
ruta_archivo = 'DATA/data_Departamentos_RM (Metropolitana)_2023-06-19.json'

# Leer el archivo JSON con pandas
df = pd.read_json(ruta_archivo)

# Imprimir el DataFrame
print(df)

df = remover_m2(df,'superficie_total')
df = remover_m2(df,'superficie_util')

#------------------------------------
cambio_CLF = 38000  
cambio_USD = 812
df['precio_CLP'] = df.apply(convertir_precio_CLP, axis=1, args=(cambio_CLF,cambio_USD,))
df.info()
#------------------------------------

# Eliminar filas donde ambas columnas son iguales a cero
df = df.drop(df[(df['superficie_total'] == 0.0) & (df['superficie_util'] == 0.0)].index)


# Obtener filas donde 'superficie_total' es igual a cero
filas_superficie_total_0 = df['superficie_total'] == 0.0

# Asignar el valor de 'superficie_util' a las filas donde 'superficie_total' es cero
df.loc[filas_superficie_total_0, 'superficie_total'] = df.loc[filas_superficie_total_0, 'superficie_util']

# Imprimir el DataFrame resultante
print(df)

# # Obtener filas donde 'superficie_total' es igual a cero
filas_superficie_util_0 = df['superficie_util'] == 0.0

# Asignar el valor de 'superficie_util' a las filas donde 'superficie_total' es cero
df.loc[filas_superficie_util_0, 'superficie_util'] = df.loc[filas_superficie_util_0, 'superficie_total']

# Imprimir el DataFrame resultante
print(df)


df["precio_metro_total"] = df.apply(metro_precio, axis=1, args=('superficie_total',))
df["precio_metro_util"] = df.apply(metro_precio, axis=1, args=('superficie_util',))


# # Crear un nuevo DataFrame con las filas que cumplen las condiciones
# #['Arriendo' 'Venta']
# #['Propiedades usadas' 'Proyectos']
df_arriendo_propiedades = df.loc[(df['categoria_2'] == 'Arriendo') & (df['categoria_3'] == 'Propiedades usadas')]

df_arriendo_propiedades = eliminar_outliers_por_ciudad(df_arriendo_propiedades,'precio_CLP', 3)
df_arriendo_propiedades = eliminar_outliers_por_ciudad(df_arriendo_propiedades,'superficie_util', 3)
df_arriendo_propiedades = eliminar_outliers_por_ciudad(df_arriendo_propiedades,'superficie_total', 3)
print(df_arriendo_propiedades)


datos_por_ciudad = df_arriendo_propiedades.groupby('cities')['precio_CLP'].agg(['mean', 'count']).sort_values(by='mean', ascending=False)
datos_por_ciudad['mean'] = datos_por_ciudad['mean'].apply(lambda x: "{:,.2f}".format(x))
print(datos_por_ciudad)

# Aplicar la función a cada grupo y obtener los resultados
minimos_5_filas = df_arriendo_propiedades.groupby("cities").apply(obtener_minimos)

datos_link_comuna = minimos_5_filas['link']
print(datos_link_comuna) #guardar


datos_por_ciudad['mean'] = datos_por_ciudad['mean'].str.replace(',', '').astype(float)

# valor_minimo = datos_por_ciudad['mean'].min()
# valor_maximo = datos_por_ciudad['mean'].max()

# cmap = LinearSegmentedColormap.from_list('heatmap', ['#0232f0', '#f00202'])

# datos_por_ciudad['normalized_mean'] = (datos_por_ciudad['mean'] - valor_minimo) / (valor_maximo - valor_minimo)
# datos_por_ciudad['color'] = datos_por_ciudad['normalized_mean'].apply(lambda x: mcolors.to_hex(cmap(x)))
# datos_por_ciudad['normalized_mean'] = datos_por_ciudad['normalized_mean'].clip(0, 1)


# Obtener valores mínimo y máximo
valor_minimo = datos_por_ciudad['mean'].min()
valor_maximo = datos_por_ciudad['mean'].max()

# Definir escala de colores divergente #minimo y maximo
cmap = LinearSegmentedColormap.from_list('diverging', ['#2ebf02', 'white', '#ff0808'])

# Calcular valores normalizados
datos_por_ciudad['normalized_mean'] = (datos_por_ciudad['mean'] - valor_minimo) / (valor_maximo - valor_minimo)
datos_por_ciudad['normalized_mean'] = datos_por_ciudad['normalized_mean'].clip(0, 1)

# Actualizar colores en el DataFrame
datos_por_ciudad['color'] = datos_por_ciudad['normalized_mean'].apply(lambda x: mcolors.to_hex(cmap(x)))



print(datos_por_ciudad) #guadar

datos_por_ciudad.to_csv('clean_data/datos_por_ciudad.csv', index=True)
datos_link_comuna.to_csv('clean_data/datos_link_comuna.csv', index=True)
#https://open-bootcamp.com/cursos/sql