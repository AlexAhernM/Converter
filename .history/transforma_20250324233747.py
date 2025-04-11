import xml.etree.ElementTree as ET


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
    
    return coords, names           
    
def extraer_coordenadas(pm):
    coords = []
    name_element = pm.find('{http://www.opengis.net/kml/2.2}name')
    name = name_element.text if name_element is not None else 'Sin nombre'
    
    ls = pm.find('{http://www.opengis.net/kml/2.2}LineString')
    if ls is not None:
        coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
        if coord is not None:
            coords.extend([c.split(',') for c in coord.text.split()])
    
    py = pm.find('{http://www.opengis.net/kml/2.2}Polygon')
    if py is not None:
        outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
        linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
        coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
        if coord is not None:
            coords.extend([c.split(',') for c in coord.text.split()])
    

