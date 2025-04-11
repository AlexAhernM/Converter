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
    
    print ("archivo ok")
    print (entrada_archivo_kml)