import zipfile
import xml.etree.ElementTree as ET

# Abrir el archivo KMZ
with zipfile.ZipFile('archivo.kmz', 'r') as kmz:
    # Extraer el archivo KML
    kml_data = kmz.read('doc.kml')

# Parsear el archivo KML
root = ET.fromstring(kml_data)

# Verificar si posee atributos de elevación
has_elevation = False
for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
    geometry = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates')
    if geometry is not None:
        coords = geometry.text.strip().split()
        for coord in coords:
            values = coord.split(',')
            if len(values) == 3:  # longitude, latitude, altitude
                has_elevation = True
                break
        if has_elevation:
            break

print(f"El archivo KML {'tiene' if has_elevation else 'no tiene'} atributos de elevación")

# Guardar el archivo KML
with open('archivo.kml', 'wb') as kml_file:
    kml_file.write(kml_data)