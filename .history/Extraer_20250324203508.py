def extraer_coord():
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
    
    return coords, name

# Extraer las coordenadas de los puntos
coords = []
names = []
for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
    coord, name = extraer_coord(pm)
    if coord:
        coords.extend(coord)
        names.extend([name] * len(coord))
        

# Extraer las coordenadas de los puntos
coords = []
names = []
for pm in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
    coord, name = extraer_coordenadas(pm)
    if coord:
        coords.extend(coord)
        names.extend([name] * len(coord))
