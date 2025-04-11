import simplekml
import gpxpy

# Cargar el archivo KML
kml = simplekml.Kml()

# Abrir el archivo KML
kml.open('archivo.kml')

# Crear un nuevo archivo GPX
gpx = gpxpy.gpx.GPX()

# Recorrer las capas del archivo KML
for folder in kml.features():
    # Recorrer los lugares del archivo KML
    for placemark in folder.features():
        # Agregar un nuevo punto de seguimiento al archivo GPX
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        gpx.tracks.append(gpx_track)

        # Agregar las coordenadas del lugar al archivo GPX
        for coord in placemark.geometry.coords:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(coord[1], coord[0], elevation=coord[2]))

# Guardar el archivo GPX
with open('archivo.gpx', 'w') as f:
    f.write(gpx.to_xml())