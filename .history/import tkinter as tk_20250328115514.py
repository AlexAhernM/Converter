import tkinter as tk
from tkinter import filedialog, ttk
import xml.etree.ElementTree as ET
import geopandas as gpd

def obtener_informacion_kml(ruta_archivo_kml):
    try:
        gdf = gpd.read_file(ruta_archivo_kml)
        
        # Data properties
        datasets_count = 1  # geopandas solo lee un archivo a la vez
        data_size = gdf.memory_usage(index=True, deep=True).sum()
        file_formats = 'KML'
        data_type = 'Vector'
        
        # Layers count
        layers_count = len(gdf)
        
        # Geometry type
        geometry_type = gdf.geom_type.iloc[0]
        
        # Features count
        features_count = len(gdf)
        
        # Coord. system
        coord_system = gdf.crs
        
        # Coord. units
        coord_units = 'degrees'
        
        # Extent (lat/lon)
        extent = gdf.total_bounds
        
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
        
    except Exception as e:
        print(f"Error leyendo el archivo KML: {e}")     
        
   
# Seleccionar el archivo KML
ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])

# Obtener la información del archivo KML
obtener_informacion_kml(ruta_archivo_kml)