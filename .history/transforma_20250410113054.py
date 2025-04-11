import tkinter as tk
import xml.etree.ElementTree as ET
import pandas as pd
import utm
import fiona
import folium
import folium
import webbrowser
import math
import ezdxf
import requests
import os

COLUMNAS = ['X', 'Y', 'Altitud', 'Capa']
obtener_elevacion_valor = tk.BooleanVar

        
zoom_levels = {
    (0 , 50) :    20, 
    (50, 100) :   19,
    (101, 200) :  18,
    (201, 500) :  18,
    (501, 999) :  17,
    (1000, 1500): 15,
    (1501, 3000): 14,
    (3001, 4500): 14,
    (4501, 8000): 13,
    (8001, 12500): 11,
    (12501, float('inf')): 10
}

def get_zoom_level(radio):
            for (min_radio, max_radio), zoom in zoom_levels.items():
                if min_radio <= radio <= max_radio:
                    return zoom
            return 10  # valor por defecto



def parseo(entrada_archivo_kml, obtener_elevacion):
    obtener_elevacion_valor = obtener_elevacion.get()
    ruta_archivo_kml = entrada_archivo_kml.get()

    try:
        tree = ET.parse(ruta_archivo_kml)
        root = tree.getroot()
     
    except ET.ParseError as e:
        print(f"Error al parsear el archivo KML: {e}")
        return
    
    print (ruta_archivo_kml)
    
    resultado = convierte(root, ruta_archivo_kml, obtener_elevacion_valor)
    coords, coords_dec = resultado

    resultados = obtener_maximos_minimos(coords, coords_dec)

    # Acceder a los resultados
    lat_min = resultados['lat_min']
    lat_max = resultados['lat_max']
    lon_min = resultados['lon_min']
    lon_max = resultados['lon_max']
    lat_centro = resultados['lat_centro']
    lon_centro = resultados['lon_centro']
    
    radio = max(abs(lat_max - lat_min), abs(lon_max - lon_min))        
    
    zoom_start = get_zoom_level(radio)
    
    print ('radio =', radio)
    print ('zoom =',  zoom_start)
    print("Latitud Centro =" , lat_centro,  "Longitu Centtro ", lon_centro)
    print ("Lat Max UTM = ", lat_max, "Lat Min UTM = ", lat_min,  "Lon Max UTM = ", lon_max, " Lon Min UTM = ", lon_min)
    
    
    
    return root,tree, ruta_archivo_kml,lat_centro, lon_centro, zoom_start, radio
    
def convierte(root, ruta_archivo_kml, obtener_elevacion_valor):
    
    layers = []  # Lista de Capas
    coords = []  # Lista de Coordenadas
    coords_dec =[]
    doc = ezdxf.new('R2000')  # Crear un nuevo documento DXF
    
    
    # Iterar sobre los elementos del archivo KML
    for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
        layer_name = name_element.text if name_element is not None else 'Sin nombre'
        
        # Verificar si el nombre ya existe en el documento DXF
        if layer_name in doc.layers:
            # Si ya existe, agregar un sufijo para hacerlo único
            i = 1
            while f"{layer_name} ({i})" in doc.layers:
                i += 1
            layer_name = f"{layer_name} ({i})"
            print (layer_name)

        ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
        py = pm.find('{http://www.opengis.net/kml/2.2}Polygon')
        mg = pm.find('{http://www.opengis.net/kml/2.2}MultiGeometry') 
        pt = pm.find('{http://www.opengis.net/kml/2.2}Point')
        #procesar lineas
        if ls is not None:
            
            # Extraer coordenadas del elemento Linestring
            coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')  
            
        # Procesar polígonos
        if py is not None:
            # Extraer el límite exterior del polígono
            outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                # Extraer el anillo lineal del límite exterior
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    # Extraer las coordenadas del elemento anillo lineal
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates') 
                    
        # Procesar puntos
        if pt is not None:
            # Extraer las coordenadas del elemento punto
            coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')             
                                               
        # Procesar MultiGeometrias        
        if mg is None:
                       
            agregar_polilinea_simple(doc, coord, layer_name,  coords, layers, obtener_elevacion_valor, coords_dec)     
        else:
            coord = mg.find('{http://www.opengis.net/kml/2.2}coordinates')
            geoms = mg.findall('{http://www.opengis.net/kml/2.2}*')
            procesar_multigeometrias(doc, coord, layer_name,   coords, layers, obtener_elevacion_valor, geoms, coords_dec)
            
               
    
    crear_dxf(doc, ruta_archivo_kml, coords, layers)
    
           
    return coords, coords_dec

def obtener_maximos_minimos(coords, coords_dec):
        
    # Calcula el promedio de las coordenadas x e y
    lats, lons = zip(*coords_dec)
    lat_centro = sum(lats) / len(lats)
    lon_centro = sum(lons) / len(lons)
      
    # Obtener los máximos y mínimos de x e y
    lat_min = min(coords, key=lambda x: x[0])[0]
    lat_max = max(coords, key=lambda x: x[0])[0]
    lon_min = min(coords, key=lambda x: x[1])[1]
    lon_max = max(coords, key=lambda x: x[1])[1]
    
    return {
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max,
        'lat_centro': lat_centro,
        'lon_centro': lon_centro
    }
     
def obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor):
    utm_points = []
    elevaciones_api = []
    
    if coord is not None:
        points = [c.split(',') for c in coord.text.split()]
        
        for point in points:
            lat, lon = float(point[1]), float(point[0])
            utm_point = utm.from_latlon(lat, lon)
            layers.append(layer_name)
            coords_dec.append((lat, lon))
            
            if obtener_elevacion_valor:
                altitud_api = obtener_altitud_api(lat, lon)
                elevaciones_api.append((lat, lon, altitud_api))
                utm_points.append((utm_point[0], utm_point[1], altitud_api))
                coords.append((utm_point[0], utm_point[1], altitud_api))
            else:
                utm_points.append((utm_point[0], utm_point[1], 0))
                coords.append((utm_point[0], utm_point[1], 0))
    
    return utm_points, coords, coords_dec, layers

def obtener_altitud_api(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyACWL7hMm-4fAymx2DY5IkJ5iDlVUy4zEA"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        print("Respuesta de la API de Google Maps recibida correctamente")
        datos = respuesta.json()
        return round(datos["results"][0]["elevation"], 2)
    else:
        return 0

def agregar_polilinea(utm_points, layer_name, doc):
    
    layer = doc.layers.new(layer_name)
    layer.dxf.color = 154  # azul (utiliza el índice de color de AutoCAD)
    msp = doc.modelspace()
    msp.add_polyline3d(utm_points, dxfattribs={'layer': layer_name, 'color': 7})

def procesar_multigeometrias(doc, coord, layer_name,   coords, layers, obtener_elevacion_valor, geoms, coords_dec):
    for geom in geoms:
        if geom.tag == '{http://www.opengis.net/kml/2.2}Polygon':
            outer_boundary = geom.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    utm_points, coords, coords_dec, layers = obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor)
                    agregar_polilinea(utm_points, layer_name, doc)
        
        elif geom.tag == '{http://www.opengis.net/kml/2.2}LineString':
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
            utm_points, coords, coords_dec, layers = obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor)
            agregar_polilinea(utm_points, layer_name, doc)
        
        elif geom.tag == '{http://www.opengis.net/kml/2.2}Point':
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
            utm_points, coords, coords_dec, layers = obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor)
            agregar_polilinea(utm_points, layer_name, doc)
    
    return coords, coords_dec, layers

def agregar_polilinea_simple(doc, coord, layer_name,   coords, layers, obtener_elevacion_valor, coords_dec):
    utm_points, coords, coords_dec, layers = obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor)
    agregar_polilinea(utm_points, layer_name, doc)
    print(f"Cantidad de elementos: {len(coords)}")
    return coords   
                
    
def crear_dxf(doc, ruta_archivo_kml, coords, layers):

   
    # Establece la carpeta Downloads del Sistema Operativo para alojar los archivos convertidos        
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    
   # 1. CAD = DXF
    # Guarda el archivo DXF
   
    nombre_archivo_salida_dxf = ruta_archivo_kml.split('/')[-1].split('.')[0] + '_utm.dxf'
    ruta_archivo_salida_dxf = os.path.join(downloads_folder, nombre_archivo_salida_dxf)

    # Renombrar el archivo si ya existe
    if os.path.exists(ruta_archivo_salida_dxf):
        base, extension = os.path.splitext(ruta_archivo_salida_dxf)
        i = 1
        while os.path.exists(ruta_archivo_salida_dxf):
            ruta_archivo_salida_dxf = f"{base} ({i}){extension}"
            i += 1

    doc.saveas(ruta_archivo_salida_dxf)
    print(f"Archivo DXF guardado correctamente en {ruta_archivo_salida_dxf}")

    # 2. SHP
    nombre_archivo_salida_shp = ruta_archivo_kml.split('/')[-1].split('.')[0] + '_utm.shp'
    ruta_archivo_salida_shp = os.path.join(downloads_folder, nombre_archivo_salida_shp)
    
    # Renombrar el archivo SHP si ya existe
    if os.path.exists(ruta_archivo_salida_shp):
        base, extension = os.path.splitext(ruta_archivo_salida_shp)
        i = 1
        while os.path.exists(ruta_archivo_salida_shp):
            ruta_archivo_salida_shp = f"{base} ({i}){extension}"
            i += 1
    
    # Abrir el archivo DXF
    with fiona.open(ruta_archivo_salida_dxf, 'r', driver='DXF') as src:
        
    
        # Crear un nuevo Shapefile
        with fiona.open(ruta_archivo_salida_shp, 'w', driver='ESRI Shapefile', schema=src.schema) as dst:
       #with fiona.open(ruta_archivo_salida_shp, 'w', driver='ESRI Shapefile', schema={'properties': src.schema['properties']}) as dst:
            
            # Agregar los datos del archivo DXF
            for feature in src:
                dst.write(feature)
    print(f"Archivo SHP guardado correctamente en {ruta_archivo_salida_shp}")
   

     # Combinar las listas en una sola lista de tuplas
    data = list(zip([point[0] for point in coords], [point[1] for point in coords], [point[2] for point in coords], layers))

    # Crear DataFrame
    df = pd.DataFrame(data, columns=COLUMNAS)

    # Comprobación para asegurarte de que el DataFrame no esté vacío
    if df.empty:
        print("No hay datos para exportar.")
        return

    # Crear la ruta del archivo de salida
    nombre_archivo_salida = f"{ruta_archivo_kml.split('/')[-1].split('.')[0]}_utm.xlsx"
    ruta_archivo_salida = os.path.join(downloads_folder, nombre_archivo_salida)

    # Renombrar el archivo si ya existe
    if os.path.exists(ruta_archivo_salida):
        base, extension = os.path.splitext(ruta_archivo_salida)
        i = 1
        while os.path.exists(ruta_archivo_salida):
            ruta_archivo_salida = f"{base} ({i}){extension}"
            i += 1

    # Exportar DataFrame a Excel
    df.to_excel(ruta_archivo_salida, index=False)
    print(f"Archivo Excel guardado correctamente en {ruta_archivo_salida}")