import tkinter as tk
from tkinter import filedialog, ttk
import fastkml
import xml.etree.ElementTree as ET

def obtener_informacion_kml(ruta_archivo_kml):
    # Abrir el archivo KML
    with open(ruta_archivo_kml, 'r') as f:
        contenido_archivo = f.read()
        kml_data = fastkml.KML()
        kml_data.from_string(f.read())
        
    # Obtener la información del archivo KML
    tree = ET.parse(ruta_archivo_kml)
    root = tree.getroot()
    namespace = '{http://www.opengis.net/kml/2.2}'
    
    # Data properties
    datasets_count = len(kml_data.features)
    data_size = len(contenido_archivo)
    file_formats = 'KML'
    data_type = 'Vector'
    
    # Layers count
    layers_count = len(kml_data.features())
    
    # Geometry type
    geometry_type = None
    for feature in kml_data.features():
        if feature.geometry is not None:
            geometry_type = feature.geometry.type
            break
    
    # Features count
    features_count = len(kml_data.features())
    
    # Coord. system
    coord_system = None
    srs_node = root.find(f'.//{namespace}SpatialReferenceSystem')
    if srs_node is not None:
        coord_system = srs_node.text
    
    # Coord. units
    coord_units = 'degrees'
    
    # Extent (lat/lon)
    extent = None
    for feature in kml_data.features:
        if feature.geometry is not None:
            extent = feature.geometry.bounds
            break
    
    # Imprimir la información
    print('Data properties:')
    print(f'Datasets count: {datasets_count}')
    print(f'Data size: {data_size} bytes')
    print(f'File formats: {file_formats}')
    print(f'Data type: {data_type}')
    print()
    print('Layers count: ', layers_count)
    print('Geometry type: ', geometry_type)
    print('Features count: ', features_count)
    print('Coord. system: ', coord_system)
    print('Coord. units: ', coord_units)
    print('Extent (lat/lon): ', extent)

# Seleccionar el archivo KML
ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])

# Obtener la información del archivo KML
obtener_informacion_kml(ruta_archivo_kml)