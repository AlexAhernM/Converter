def crear_dxf(doc, ruta_archivo_kml, coords, layers, coords_dec):

    # Establece la carpeta Downloads del Sistema Operativo para alojar los archivos convertidos        
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    
   # 1. CAD = DXF
    
    # Calcular las coordenadas de extensión
    x_coords = [point[0] for point in coords]
    y_coords = [point[1] for point in coords]
    ext_min = (min(x_coords), min(y_coords), 0)
    ext_max = (max(x_coords), max(y_coords), 0)

    doc.header['$EXTMIN'] = ext_min
    doc.header['$EXTMAX'] = ext_max
    
   
    doc.header['$EXTMIN'] = ext_min
    doc.header['$EXTMAX'] = ext_max

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
        # Crear un nuevo Shapefile para líneas
        with fiona.open(ruta_archivo_salida_shp, 'w', driver='ESRI Shapefile', crs=src.crs, schema={'geometry': 'LineString', 'properties': src.schema['properties']}) as dst_lineas:
            # Agregar los datos del archivo DXF
            for feature in src:
                if feature.geometry.type == 'Polygon':
                    new_feature = {
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': feature.geometry.coordinates[0]
                        },
                        'properties': feature.properties
                    }
                    dst_lineas.write(new_feature)
                elif feature.geometry.type == 'LineString':
                    dst_lineas.write(feature)

    print(f"Archivo SHP guardado correctamente en {ruta_archivo_salida_shp}")
    
     # Combinar las listas en una sola lista de tuplas
    data = list(zip([point[0] for point in coords_dec],[point[1] for point in coords_dec], [point[0] for point in coords], [point[1] for point in coords], [point[2] for point in coords], layers))

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