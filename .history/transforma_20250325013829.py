import xml.etree.ElementTree as ET
import pandas as pd
import ezdxf.colors
import utm
import os
import ezdxf
import geopandas as gpd
from shapely.geometry import Point, Polygon

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
    
    # Extraer las coordenadas de los puntos
    coords = []
    names = []
    for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
            coord, name = extraer_coordenadas(pm)
            if coord:
                coords.extend(coord)
                names.extend([name] * len(coord))
    
    # Convertir las coordenadas a UTM
    utm_coords = []
    for coord, name in zip(coords, names):
        try:
            lon, lat, alt = map(float, coord)
            utm_coord = utm.from_latlon(lat, lon)
            utm_coords.append([utm_coord[0], utm_coord[1], name])
        except Exception as e:
            print("Error al convertir coordenada:", e)

    # Generar archivo Excel
    df = pd.DataFrame(utm_coords, columns=['X UTM', 'Y UTM', 'Nombre'])
    # Obtener la ruta de la carpeta Downloads
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    nombre_archivo_salida = ruta_archivo_kml.split('/')[-1].split('.')[0] + '_utm.xlsx'
    ruta_archivo_salida = os.path.join(downloads_folder, nombre_archivo_salida)
    if os.path.exists(ruta_archivo_salida):
        base, extension = os.path.splitext(ruta_archivo_salida)
        i = 1
        while os.path.exists(ruta_archivo_salida):
            ruta_archivo_salida = f"{base} ({i}){extension}"
            i += 1
    while True:
        if os.path.exists(ruta_archivo_salida):
            print("El archivo está abierto. Por favor, ciérrelo.")
            input("Presione Enter para continuar...")
            continue
        else:
            try:
                df.to_excel(ruta_archivo_salida, index=False)
                print("Archivo transformado y guardado con éxito.")
                break
            except Exception as e:
                print("Error al guardar el archivo:", e)
                break

    print("Archivo transformado y guardado con éxito.")
    

    # Generar archivo DXF
    doc = ezdxf.new('R2000')
    doc.name = nombre_archivo_salida.split('.')[0]

  
   # Generar archivo DXF
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    # Lista de tuplas con coordenadas y nombres
    elements = []

    for name, coords in zip(names, utm_coords):
        # Validar coordenadas
        if not all(isinstance(x, (int, float)) for x in coords):
            print(f"Error: Coordenadas inválidas para {name}")
            continue
        
        # Agregar puntos
        if len(coords) == 2:
            elements.append((name, 'point', (coords[0], coords[1])))
        
        # Agregar polilíneas o polígonos
        else:
            # Convertir coordenadas a formato [(x, y), (x, y), ...]
            coords = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
            
            # Agregar polilíneas
            if coords[0] != coords[-1]:
                elements.append((name, 'lwpolyline', coords))
            
            # Agregar polígonos
            else:
                elements.append((name, 'polygon', coords))

    # Agregar elementos a la capa
    for name, element_type, coords in elements:
        if element_type == 'point':
            msp.add_point(coords, dxfattribs={'layer': name})
        elif element_type == 'lwpolyline':
            msp.add_lwpolyline(coords, dxfattribs={'layer': name})
        elif element_type == 'polygon':
            msp.add_polygon(coords, dxfattribs={'layer': name})

    # Guarda el archivo DWG
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
    
    # Generar archivo Shapefile
    geoms = []
    for coord, name in zip(utm_coords, names):
        geoms.append(Point(coord[:2]))
    gdf = gpd.GeoDataFrame(utm_coords, columns=['X UTM', 'Y UTM', 'Nombre'], geometry=geoms)
    
    return coords, names           
    
def extraer_coordenadas(pm):
    coords = []
    name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
    name = name_element.text if name_element is not None else 'Sin nombre'
    
    # Buscar coordenadas en LineString
    ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
    if ls is not None:
        coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
        if coord is not None:
            coords.extend([c.split(',') for c in coord.text.split()])
    
    # Buscar coordenadas en MultiGeometry/Polygon
    mg = pm.find('{http://www.opengis.net/kml/2.2}MultiGeometry')
    if mg is not None:
        poly = mg.find('{http://www.opengis.net/kml/2.2}Polygon')
        if poly is not None:
            outer_boundary = poly.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
            coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
            if coord is not None:
                coords.extend([c.split(',') for c in coord.text.split()])
    
    return coords, name


