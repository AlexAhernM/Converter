import xml.etree.ElementTree as ET
import pandas as pd
import ezdxf.colors
import utm
import fiona
import os
import numpy as np
import ezdxf



def transformar_archivo_kml(entrada_archivo_kml):
    ruta_archivo_kml = entrada_archivo_kml.get()
    
    # Leer el archivo KML
    try:
        tree = ET.parse(ruta_archivo_kml)
        root = tree.getroot()  # Agregar esta línea
    except ET.ParseError as e:
        print(f"Error al parsear el archivo KML: {e}")
        return
    
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
    
    nombre_archivo_salida = ruta_archivo_kml.split('/')[-1].split('.')[0] + '_utm.xlsx'
    
    # Crear un nuevo documento DXF
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()
    
    # Asigna un nombre al documento
    doc.name = nombre_archivo_salida.split('.')[0]
  
    # Iterar sobre los elementos del archivo KML
    names = []
    utm_points = []
    coords = []
    coords_shp =[]
    layers = []
    color_index =0
    for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
        layer_name = name_element.text if name_element is not None else 'Sin nombre' 
          
        #Procesar Lineas
        ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
        if ls is not None:
            #Crear capa en modelo espacio CAD
            layer = doc.layers.new(layer_name)
            layer.dxf.color = 154  # azul (utiliza el índice de color de AutoCAD)
            
            #Extraer coordenadas del elemento Linestring
            coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
            points = [c.split(',') for c in coord.text.split()]
            
            #Extraer el  modo de altitud (altitudMode) y establecer valor por defecto si altitud mode = None
            altitude_mode = ls.find('{http://www.opengis.net/kml/2.2}altitudeMode')
            altitude_mode = altitude_mode.text if altitude_mode is not None else 'clampToGround'   
            
            #Convertir las  coordenas a UTM y agregar la polilinea al espacio de modeolo CAD
            for point in points:
                lat, lon, z = float(point[1]), float(point[0]), float(point[2])
                if altitude_mode =='relativeToGround':
                    # La coordenada Z es relativa al terreno
                    z = z
                elif altitude_mode=='absolute':
                    #la coordenada Z es absoluta
                    z= z 
                else:
                    # la coordenada Z se ignora (clampToGround)
                    z=0
                utm_point = utm.from_latlon(lat, lon)
                names.append(layer_name)
                utm_points.append((utm_point[0], utm_point[1],z))
                coords.append((utm_point[0], utm_point[1],z))
                layers.append(layer_name)
                
            msp.add_lwpolyline(utm_points, dxfattribs={'layer': layer_name,'color': 7 }) 
            utm_points = [] # limpiar la lista
            
        #Procesar Poligonos
        py = pm.find('{http://www.opengis.net/kml/2.2}Polygon')
        outer_boundary = None
        if py is not None:
            outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                #Extraer el anillo lineal del limiete exterior
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                
                if linear_ring is not None:
                    #Extraer las coordenadas del anillo lineal
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    
                    if coord is not None:
                        #Dividir las coordenadas en puntos individuales
                        points = [c.split(',') for c in coord.text.split()]
                        
                        #Extraer el modo de altitud (altitudMode)
                        altitude_mode = py.find('{http://www.opengis.net/kml/2.2}altitudeMode')
                        if altitude_mode is not None:
                            altitude_mode = altitude_mode.text
                        else:
                            altitude_mode = 'clampToGround'
                            
                    # Convertir las coordenadas a UTM y agregar la polilínea al espacio de modelo
                    for point in points:
                        lat, lon, z= float(point[1]), float(point[0]),float(point[2])
                        if altitude_mode == 'relativeToGround':
                        # La coordenada Z es relativa al terreno
                            z = z
                        elif altitude_mode == 'absolute':
                        # La coordenada Z es absoluta
                            z = z
                        else:
                        # La coordenada Z se ignora (clampToGround)
                            z = 0
                        utm_point = utm.from_latlon(lat, lon)
                        names.append(layer_name)
                        utm_points.append((utm_point[0], utm_point[1],z))
                        coords.append((utm_point[0], utm_point[1],z))
                        layers.append(layer_name)
                    msp.add_lwpolyline(utm_points, dxfattribs={'layer': layer_name,'color':7})          
                    utm_points = [] # limpiar la lista
         
        # Procesar MultiGeometrias
        mg = pm.find('{http://www.opengis.net/kml/2.2}MultiGeometry')   
        if mg is not None:
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
                                    utm_points.append((utm_point[0], utm_point[1]))
                                    coords.append((utm_point[0], utm_point[1]))
                                    coords_shp.append((lat, lon))
                                    layers.append(layer_name)
                                msp.add_lwpolyline(utm_points, dxfattribs={'layer': layer_name})
                                utm_points=[] # limpia la lista
                            
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
                            coords_shp.append((lat, lon))
                            layers.append(layer_name)
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
                            utm_points.append((utm_point[0], utm_point[1]))
                            coords.append((utm_point[0], utm_point[1]))
                            coords_shp.append((lat, lon))
                            layers.append(layer_name)
                        msp.add_point(utm_points,dxfattribs={'layer': layer_name}) 
                        utm_points=[] # limpiar lista        
        
        # Procesar Puntos               
        pt = pm.find('{http://www.opengis.net/kml/2.2}Point')
        if pt is not None:
            coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')
            point = coord.text.split(',')
            for point in points:
                lat, lon,z = float(point[1]), float(point[0]), float(point[2])
                utm_point = utm.from_latlon(lat, lon)
                coords.append((utm_point[0], utm_point[1]))
                coords_shp.append((lat, lon))
                layers.append(layer_name)
            msp.add_point((utm_point[0], utm_point[1]),dxfattribs={'layer': layer_name})
            
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
   
    # 3. EXCEL
    
    # Combinar las listas en una sola lista de tuplas
    data = list(zip([point[0] for point in coords], [point[1] for point in coords], [point[2] in coords], layers))

    # Crear  DataFrame
    df = pd.DataFrame(data, columns=['X', 'Y', 'Altitud', 'Capa'])
    
    # Exportar  DataFrame a  Excel
    nombre_archivo_salida = ruta_archivo_kml.split('/')[-1].split('.')[0] + '_utm.xlsx'
    ruta_archivo_salida = os.path.join(downloads_folder, nombre_archivo_salida)
   
    # Renombrar el archivo si ya existe
    if os.path.exists(ruta_archivo_salida):
        base, extension = os.path.splitext(ruta_archivo_salida)
        i = 1
        while os.path.exists(ruta_archivo_salida):
            ruta_archivo_salida = f"{base} ({i}){extension}"
            i += 1
    df.to_excel(ruta_archivo_salida, index=False)
    print(f"Archivo Excel guardado correctamente en {ruta_archivo_salida}")   
