import requests

def obtener_elevacion(latitud, longitud):
    """
    Obtiene la elevación de un punto dado su longitud y latitud.

    Args:
        latitud (float): La latitud del punto.
        longitud (float): La longitud del punto.

    Returns:
        float: La elevación del punto en metros.
    """
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitud},{longitud}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        elevacion = datos["results"][0]["elevation"]
        return elevacion
    else:
        return None

# Ejemplo de uso
latitud = -33.028772149
longitud = -71.627887806
elevacion = obtener_elevacion(latitud, longitud)

if elevacion is not None:
    print(f"La elevación del punto es {elevacion} metros")
else:
    print("No se pudo obtener la elevación")