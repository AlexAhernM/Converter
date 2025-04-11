import tkinter as tk
import xml.etree.ElementTree as ET
import pandas as pd
import ezdxf.colors
import utm
import fiona
import numpy as np
import ezdxf
import requests
import os

# Definir constantes para los nombres de las columnas
COLUMNAS = ['X', 'Y', 'Altitud', 'Capa']

obtener_elevacion_valor = tk.BooleanVar

def parseo(entrada_archivo_kml, obtener_elevacion):
    
    obtener_elevacion_valor = obtener_elevacion.get()
    
    ruta_archivo_kml = entrada_archivo_kml.get()
    
    # Leer el archivo KML
    try:
        tree = ET.parse(ruta_archivo_kml)
        root = tree.getroot()  # Agregar esta línea
        
    except ET.ParseError as e:
        print(f"Error al parsear el archivo KML: {e}")
        return
    
    print (ruta_archivo_kml)
     # Busca todos los estilos en el documento
    estilos = []
    estilos = root.findall('.//{http://www.opengis.net/kml/2.2}Style')

    # Normaliza los estilos
    for estilo in estilos:
        if estilo.find('{http://www.opengis.net/kml/2.2}styleMap') is not None:
            style_map = estilo.find('{http://www.opengis.net/kml/2.2}styleMap')
            if style_map.find('{http://www.opengis.net/kml/2.2}normalStyle') is not None:
                normal_style = style_map.find('{http://www.opengis.net/kml/2.2}normalStyle')
                if normal_style.find('{http://www.opengis.net/kml/2.2}lineStyle') is not None:
                    line_style = normal_style.find('{http://www.opengis.net/kml/2.2}lineStyle')
                    line_style.find('{http://www.opengis.net/kml/2.2}color').text = 'ff0000ff'
                if normal_style.find('{http://www.opengis.net/kml/2.2}polyStyle') is not None:
                    poly_style = normal_style.find('{http://www.opengis.net/kml/2.2}polyStyle')
                    poly_style.find('{http://www.opengis.net/kml/2.2}color').text = 'ff0000ff'
    

    
    tree.write(ruta_archivo_kml)
    utm_points =[]
    names = []
    layers = []  # Lista de Capas
    coords = []  # Lista de Coordenadas
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()
    
    # Iterar sobre los elementos del archivo KML
    for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
        layer_name = name_element.text if name_element is not None else 'Sin nombre' 
        
        ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
        py = pm.find('{http://www.opengis.net/kml/2.2}Polygon')
        mg = pm.find('{http://www.opengis.net/kml/2.2}MultiGeometry') 
        pt = pm.find('{http://www.opengis.net/kml/2.2}Point')
        #procesar lineas
        if ls is not None:
            layer = doc.layers.new(layer_name)
            layer.dxf.color = 154  # azul (utiliza el índice de color de AutoCAD)
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
                    # Extraer las coordenadas del anillo lineal
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates') 
                    
        # Procesar puntos
        if pt is not None:
            coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')             
                                   
                
        # Procesar MultiGeometrias        
        if mg is None:             
            agregar_polilinea(coord, layer_name, doc,  coords, layers, obtener_elevacion_valor)     
        else:
            procesar_multigeometrias(mg, coord, coords, utm_points, names, layer_name, layers, msp, ruta_archivo_kml, doc)
            
    return coord, layer_name
                
def procesar_multigeometrias(mg, coord, coords, utm_points, names, layer_name, layers, msp, ruta_archivo_kml, doc):
    coord = mg.find('{http://www.opengis.net/kml/2.2}coordinates')
    geoms = mg.findall('{http://www.opengis.net/kml/2.2}*')
    for geom in geoms:
                    
        #Procesar los poligonos en MultiGeometria
        if geom.tag == '{http://www.opengis.net/kml/2.2}Polygon':
            outer_boundary = geom.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    if coord is not None:
                        points = [c.split(',') for c in coord.text.split()]
                        for point in points:
                            lat, lon = float(point[1]), float(point[0])
                            utm_point = utm.from_latlon(lat, lon)
                            names.append(layer_name)
                            utm_points.append((utm_point[0], utm_point[1],0))
                            coords.append((utm_point[0], utm_point[1],0))
                            layers.append(layer_name) 
                       
                # Procesar las líneas en Multigeometria
                elif geom.tag == '{http://www.opengis.net/kml/2.2}LineString':
                    coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
                    
                # Procesar los puntos en Multigeometria
                elif geom.tag == '{http://www.opengis.net/kml/2.2}Point':
                    coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
    
        print (f'Cantidad de elementos = {len(coords)}')
        msp.add_lwpolyline(utm_points, dxfattribs={'layer': layer_name})
        utm_points=[] # limpia la lista
    
    crear_dxf(ruta_archivo_kml, doc, coords, layers)
    return coord, layer_name                
        

def agregar_polilinea (coord, layer_name, doc,  coords, layers, obtener_elevacion_valor):
    names = []
    utm_points = []
    elevaciones_api = []
    
    # Crear un nuevo documento DXF
    
    msp = doc.modelspace()
    
    if coord is not None:
        points = [c.split(',') for c in coord.text.split()]

    # Convertir las coordenadas a UTM y 
        for point in points:
            lat, lon, = float(point[1]), float(point[0])
            utm_point = utm.from_latlon(lat, lon)
            names.append(layer_name)
            layers.append(layer_name)
            if obtener_elevacion_valor:
                #Obtener la altitud utilizando la API de Google Maps, generar listas con  coordenadas y capas
                url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyACWL7hMm-4fAymx2DY5IkJ5iDlVUy4zEA"
                respuesta = requests.get(url)
                                
                if respuesta.status_code == 200:
                    print("Respuesta de la API de Google Maps recibida correctamente")
                    datos = respuesta.json()
                    altitud_api = round(datos["results"][0]["elevation"], 2)
                    elevaciones_api.append((lat, lon, altitud_api))
                    utm_points.append((utm_point[0], utm_point[1], altitud_api))
                    coords.append((utm_point[0], utm_point[1], altitud_api))
                    print(f"Latitud: {point[0]}, Longitud: {point[1]}, Altitud: {altitud_api} metros")
                    
            #else:
            utm_points.append((utm_point[0], utm_point[1],0))
            coords.append((utm_point[0], utm_point[1]),0)
                #print(f"Latitud: {utm_point[0]}, Longitud: {utm_point[1]}")
           

    #agregar la polilínea al espacio de modelo
    print (f'Cantidad de elementos = {len(coords),0}')       
    msp.add_polyline3d(utm_points, dxfattribs={'layer': layer_name, 'color': 7})
    utm_points = []  # limpiar la lista
    
    
        
    return coords, layers

    
def crear_dxf(ruta_archivo_kml, doc, coords, layers):

   
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