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
        
    return root,tree, ruta_archivo_kml,lat_centro, lon_centro, zoom_start, radio
    
def procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec):
    utm_points, coords, coords_dec, layers = obtener_coordenadas(coord, layer_name, coords, coords_dec, layers, obtener_elevacion_valor)
    agregar_polilinea(utm_points, layer_name, doc)
    return coords, coords_dec, layers


def procesar_multigeometrias(doc, geoms, layer_name, coords, layers, obtener_elevacion_valor, coords_dec):
    for geom in geoms:
        if geom.tag == '{http://www.opengis.net/kml/2.2}Polygon':
            outer_boundary = geom.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
        elif geom.tag == '{http://www.opengis.net/kml/2.2}LineString':
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
            coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
        elif geom.tag == '{http://www.opengis.net/kml/2.2}Point':
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
            coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
    
    return coords, coords_dec, layers

def convierte(root, ruta_archivo_kml, obtener_elevacion_valor):
    layers = []  # Lista de Capas
    coords = []  # Lista de Coordenadas
    coords_dec =[]
    doc = ezdxf.new('R2013')  # Crear un nuevo documento DXF
    
    
    # Iterar sobre los elementos del archivo KML
    for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
        layer_name = name_element.text if name_element is not None else 'Sin nombre'
    
            
        # Encontrar las geometrias en Placemark (pm)
        ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
        py = pm.find('{http://www.opengis.net/kml/2.2}Polygon')
        mg = pm.find('{http://www.opengis.net/kml/2.2}MultiGeometry') 
        pt = pm.find('{http://www.opengis.net/kml/2.2}Point')
            
        if ls is not None:
            coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
            coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
                
        elif py is not None:
            outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
                        
        elif mg is not None:
            coords, coords_dec, layers = procesar_multigeometrias(doc, mg, layer_name, coords, layers, obtener_elevacion_valor, coords_dec)
                
        elif pt is not None:
            coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')
            coords, coords_dec, layers = procesar_geometria(doc, coord, layer_name, coords, layers, obtener_elevacion_valor, coords_dec) 
    
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
    # Verificar si el nombre ya existe en el documento DXF
    if layer_name in doc.layers:
        # Si ya existe, agregar un sufijo para hacerlo único
        i = 1
        while f"{layer_name} ({i})" in doc.layers:
            i += 1
        layer_name = f"{layer_name} ({i})"    
    layer = doc.layers.new(layer_name)
    layer.dxf.color = 154  # azul (utiliza el índice de color de AutoCAD)
    msp = doc.modelspace()
    
    if len(utm_points) == 1:  # Si es un punto
        # Generar un círculo de radio un metro alrededor del punto
        radius = 1  # Radio del círculo en metros
        num_points = 36  # Número de puntos que conforman el círculo
        circle_points = []
        for i in range(num_points):
            angle = i * 360 / num_points
            x = utm_points[0][0] + radius * math.cos(math.radians(angle))
            y = utm_points[0][1] + radius * math.sin(math.radians(angle))
            circle_points.append((x, y))
        # Agregar el círculo al documento DXF
        
        msp.add_polyline2d(circle_points, dxfattribs={'layer': layer_name, 'color': 7})
        
    else:
        # Agregar la polilínea al documento DXF
        
        msp.add_polyline3d(utm_points, dxfattribs={'layer': layer_name, 'color': 7})
    
                
    
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
        # Crear un nuevo Shapefile para puntos
        ruta_archivo_salida_shp_puntos = ruta_archivo_salida_shp.replace('.shp', '_puntos.shp')
        with fiona.open(ruta_archivo_salida_shp_puntos, 'w', driver='ESRI Shapefile', schema={'geometry': 'Point', 'properties': src.schema['properties']}) as dst_puntos:
            # Crear un nuevo Shapefile para líneas
            ruta_archivo_salida_shp_lineas = ruta_archivo_salida_shp.replace('.shp', '_lineas.shp')
            with fiona.open(ruta_archivo_salida_shp_lineas, 'w', driver='ESRI Shapefile', schema={'geometry': 'LineString', 'properties': src.schema['properties']}) as dst_lineas:
                # Agregar los datos del archivo DXF
                for feature in src:
                    if feature.geometry.type == 'Point':
                        dst_puntos.write(feature)
                    elif feature.geometry.type == 'LineString':
                        dst_lineas.write(feature)
                        
    print(f"Archivo SHP guardado correctamente en {ruta_archivo_salida_shp_puntos} y {ruta_archivo_salida_shp_lineas}")
   

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