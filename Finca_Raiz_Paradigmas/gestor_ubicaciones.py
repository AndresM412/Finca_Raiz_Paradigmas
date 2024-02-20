from geopy.geocoders import Nominatim
from casas import casas
import math

class GestorUbicaciones:

    @staticmethod
    def obtener_direccion(latitud: float, longitud: float) -> str:
        geolocator = Nominatim(user_agent="mi_aplicacion")
        ubicacion = f"{latitud}, {longitud}"
        location = geolocator.reverse(ubicacion)

        direccion = ""
        municipio = ""
        if 'address' in location.raw:
            address = location.raw['address']
            partes_direccion = []
            if 'road' in address or 'house_number' in address:
                road = address.get('road', '')
                house_number = address.get('house_number', '')
                if road and house_number:
                    partes_direccion.append(f"{road} # {house_number}")
                else:
                    partes_direccion.append(road or house_number)
            if 'suburb' in address:
                partes_direccion.append(address['suburb'])

            direccion = ", ".join(partes_direccion)

            if 'town' in address:
                municipio = address['town']
            elif 'city' in address:
                municipio = address['city']
            elif 'village' in address:
                municipio = address['village']

        return f"{direccion}, {municipio}".strip(", ")

    @staticmethod
    def calcular_distancia(latitud1, longitud1, latitud2, longitud2):
        radio_tierra = 6371  
        latitud1 = math.radians(latitud1)
        longitud1 = math.radians(longitud1)
        latitud2 = math.radians(latitud2)
        longitud2 = math.radians(longitud2)

        diferencia_latitudes = latitud2 - latitud1
        diferencia_longitudes = longitud2 - longitud1

        a = math.sin(diferencia_latitudes / 2) ** 2 + math.cos(latitud1) * math.cos(latitud2) * math.sin(diferencia_longitudes / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distancia = radio_tierra * c
        return distancia

    @staticmethod
    def traducir_coordenadas(direc: str):
        geolocator = Nominatim(user_agent="mi_app")
        location = geolocator.geocode(direc)
        if location is not None:
            return location.latitude, location.longitude
        else:
            return None, None

    @classmethod
    def marcado(cls, refe):
        cerca = []
        principalla, principallon = cls.traducir_coordenadas(refe)
        if principalla is None or principallon is None:
            return "Dirección de referencia no encontrada"

        for direccion, precio, tipo in casas:
            acompla, acomplon = cls.traducir_coordenadas(direccion)
            if acompla is None or acomplon is None:
                continue  # Salta esta iteración si la dirección no se pudo traducir
            dist = cls.calcular_distancia(principalla, principallon, acompla, acomplon)

            if dist < 2:
                cerca.append(f"{direccion} a {dist:.2f} Km - Precio: ${precio} - Tipo: {tipo}")

        return "No hay más casas cercanas" if not cerca else cerca




