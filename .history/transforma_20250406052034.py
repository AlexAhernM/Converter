import tkinter as tk
import xml.etree.ElementTree as ET
import pandas as pd
import ezdxf.colors
import utm
import fiona
import folium
import geopandas as gpd
import folium
import webbrowser
from fastkml import kml
import numpy as np
import ezdxf
import requests
import os

COLUMNAS = ['X', 'Y', 'Altitud', 'Capa']
obtener_elevacion_valor = tk.BooleanVar
lat_centro = 0.0
lon_centro = 0.0
ruta_archivo_kml = str

class Mapa:
    def __init__(self, lat_centro, lon_centro):
        self.mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=14)  

    def agregar_datos(self, lat_centro, lon_centro):
        folium.Circle([lat_centro, lon_centro], radius=3000, color='blue').add_to(self.mapa)

    def guardar_mapa(self):
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.mapa.save(os.path.join(downloads_folder, 'mapa.png'))
        self.mapa.save('mapa.html')

    def abrir_mapa(self):
        webbrowser.open("mapa.html")


def parseo(entrada_archivo_kml, obtener_elevacion):
    obtener_elevacion_valor = obtener_elevacion.get()
    ruta_archivo_kml = entrada_archivo_kml.get()

    try:
        tree = ET.parse(ruta_archivo_kml)
        root = tree.getroot()
        
        lat_min = float('inf')
        lat_max = float('-inf')
        lon_min = float('inf')
        lon_max = float('-inf')
         

        for elem in root.iter():
            if elem.tag.endswith('coordinates'):
                coords = elem.text.split(',')
                lat  = float(coords[1])
                lon = float(coords[0])
                
                lat_min = min(lat_min, lat)
                lat_max = max(lat_max, lat)
                lon_min = min(lon_min, lon)
                lon_max = max(lon_max, lon)
                
        lat_centro = (lat_max - lat_min) / 2
        lon_centro = (lon_max - lon_min) / 2
                
        radio = max(lat_max - lat_min, lon_max - lon_min) / 2
                

        print(lat_centro, lon_centro)
        mapa = Mapa(lat_centro, lon_centro)
        mapa.agregar_datos(lat_centro, lon_centro)
        mapa.guardar_mapa()
        mapa.abrir_mapa()

    except ET.ParseError as e:
        print(f"Error al parsear el archivo KML: {e}")
        return
    
    print (ruta_archivo_kml)
    
    
    
    tree.write(ruta_archivo_kml)
    
    convierte(root, ruta_archivo_kml, obtener_elevacion_valor)
    return root,tree, ruta_archivo_kml, lat_centro, lon_centro, radio
    
def convierte(root, ruta_archivo_kml, obtener_elevacion_valor):
    
    layers = []  # Lista de Capas
    coords = []  # Lista de Coordenadas
    doc = ezdxf.new('R2000')
    
    
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
            coord = mg.find('{http://www.opengis.net/kml/2.2}coordinates')
            geoms = mg.findall('{http://www.opengis.net/kml/2.2}*')
            procesar_multigeometrias(coord, layer_name, doc,  coords, layers, obtener_elevacion_valor, geoms)
            
    crear_dxf(ruta_archivo_kml, doc, coords, layers)       
    return
                
def procesar_multigeometrias(coord, layer_name, doc,  coords, layers, obtener_elevacion_valor, geoms):
    names = []
    utm_points = []
    elevaciones_api = []

    msp = doc.modelspace()
    
    
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
                            
                            else:
                                utm_points.append((utm_point[0], utm_point[1],0))
                                coords.append((utm_point[0], utm_point[1],0))
                            
                print(f"Cantidad de elementos multigeometria tipo poligono: {len(coords)}")       
                msp.add_polyline3d(utm_points, dxfattribs={'layer': layer_name, 'color': 7})
                utm_points = []  # limpiar la lista
                       

                # Procesar las líneas en Multigeometria
            elif geom.tag == '{http://www.opengis.net/kml/2.2}LineString':
                coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
                if coord is not None:
                        points = [c.split(',') for c in coord.text.split()]
                        for point in points:
                            lat, lon = float(point[1]), float(point[0])
                            utm_point = utm.from_latlon(lat, lon)
                            names.append(layer_name)
                            utm_points.append((utm_point[0], utm_point[1]))
                            coords.append((utm_point[0], utm_point[1]))
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
                            else:
                                utm_points.append((utm_point[0], utm_point[1],0))
                                coords.append((utm_point[0], utm_point[1],0))
                                
                        print (f'Cantidad de elementos tipo linea = {len(coords)}')
                        msp.add_lwpolyline(utm_points, dxfattribs={'layer': layer_name})
                        utm_points = [] # limpiar la lista
                    
            # Procesar los puntos en Multigeometria
            elif geom.tag == '{http://www.opengis.net/kml/2.2}Point':
                coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
                if coord is not None:
                        point = coord.text.split(',')
                        for point in points:
                            lat, lon = float(point[1]), float(point[0])
                            utm_point = utm.from_latlon(lat, lon)
                            names.append(layer_name)
                            utm_points.append((utm_point[0], utm_point[1],0))
                            coords.append((utm_point[0], utm_point[1]),0)
                            layers.append(layer_name)
                        msp.add_point(utm_points,dxfattribs={'layer': layer_name}) 
                        utm_points=[] # limpiar lista 

    return   
        

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
                    
            
            else:
                utm_points.append((utm_point[0], utm_point[1], 0))                           
                coords.append((utm_point[0], utm_point[1], 0))
                #print(f"Latitud: {utm_point[0]}, Longitud: {utm_point[1]}")
           

    #agregar la polilínea al espacio de modelo
    print(f"Cantidad de elementos: {len(coords)}")       
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