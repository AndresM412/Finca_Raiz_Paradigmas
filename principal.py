import tkinter as tk
import webbrowser
from geopy.geocoders import Nominatim
import math


class InterfazGUI:
    def __init__(self):
        self.gestor_ubicaciones = GestorUbicaciones()  # Instancia de GestorUbicaciones
        self.ventana_principal = tk.Tk()
        self.configurar_ventana()

    def configurar_ventana(self):
        self.ventana_principal.title("Ubicación y Mapa con Tkinter")
        self.ventana_principal.geometry("600x400")
        self.ventana_principal.configure(bg='red')

        # Configurar etiqueta de instrucción, entrada, botones y etiqueta de ubicación
        self.etiqueta_instruccion = tk.Label(self.ventana_principal, text="Ingresa tu dirección y presiona 'Buscar':")
        self.etiqueta_instruccion.pack(pady=10)

        self.entrada_direccion = tk.Entry(self.ventana_principal, width=50)
        self.entrada_direccion.pack(pady=5)

        self.boton_buscar_direccion = tk.Button(self.ventana_principal, text="Buscar", command=self.buscar_direccion)
        self.boton_buscar_direccion.pack(pady=10)

        self.etiqueta_ubicacion = tk.Label(self.ventana_principal, text="")
        self.etiqueta_ubicacion.pack(pady=10)

        # Botón para buscar direcciones cercanas
        self.boton_buscar_cercanas = tk.Button(self.ventana_principal, text="Buscar Direcciones Cercanas", command=self.mostrar_direcciones_cercanas)
        self.boton_buscar_cercanas.pack(pady=10)
        

    def mostrar_direcciones_cercanas(self):
        direccion_referencia = self.entrada_direccion.get()
        if direccion_referencia:
            direcciones_cercanas = self.gestor_ubicaciones.marcado(self.gestor_ubicaciones.casas, direccion_referencia)
            self.abrir_ventana_direcciones(direcciones_cercanas)
        else:
            self.etiqueta_ubicacion.config(text="Por favor, ingresa una dirección de referencia.")

    def abrir_ventana_direcciones(self, direcciones):
        ventana_direcciones = tk.Toplevel(self.ventana_principal)
        ventana_direcciones.title("Direcciones Cercanas")
        ventana_direcciones.geometry("400x300")
        texto_direcciones = "\n".join(direcciones) if direcciones else "No se encontraron direcciones cercanas."
        tk.Label(ventana_direcciones, text=texto_direcciones, justify=tk.LEFT).pack(pady=10, padx=10)

    def buscar_direccion(self):
        direccion = self.entrada_direccion.get()  # Obtener la dirección del campo de entrada
        if direccion:
            ubicacion = GestorUbicaciones()
            lat, lon = ubicacion.traducir_coordenadas(direccion)
            if lat and lon:
                self.mostrar_mapa(lat, lon)
                self.etiqueta_ubicacion.config(text="Ubicación encontrada. Abriendo mapa...")
            else:
                self.etiqueta_ubicacion.config(text="Dirección no encontrada.")
        else:
            self.etiqueta_ubicacion.config(text="Por favor, ingresa una dirección.")

    def mostrar_mapa(self, latitud, longitud):
        url_mapa = f"https://www.openstreetmap.org/?mlat={latitud}&mlon={longitud}#map=12/{latitud}/{longitud}"
        webbrowser.open(url_mapa)


import tkinter as tk
import webbrowser
from geopy.geocoders import Nominatim
import math
import requests

class GestorUbicaciones:
    # Código de la clase Ubicacion aquí, sin cambios significativos
    casas = [
        ["Calle 10 # 43-50, medellín"],
        ["Carrera 45 # 24-61, medellín"],
        ["Avenida 33 # 59-21, medellín"],
        ["Calle 11 # 36-55, medellín"],
        ["Carrera 50 # 22-15, medellín"],
        ["Calle 34 # 53-28, medellín"],
        ["Calle 9 # 39-43, medellín"],
        ["Carrera 48 # 25-12, medellín"],
        ["Calle 32 # 56-37, medellín"],
        ["Calle 12 # 32-59, medellín"],
        ["Carrera 49 # 23-21, medellín"],
        ["Calle 35 # 50-49, medellín"],
        ["Calle 8 # 45-30, medellín"],
        ["Carrera 47 # 26-41, medellín"],
        ["Calle 31 # 58-23, medellín"],
        ["Calle 11 # 45-50, medellín"],
        ["Carrera 51 # 22-35, medellín"],
        ["Calle 36 # 52-18, medellín"],
        ["Calle 7 # 41-39, medellín"],
        ["Carrera 46 # 27-29, medellín"],
        ["Carrera 70 # 29-13, itagüí"]
    ]


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
        radio_tierra = 6371  # Radio de la Tierra en kilómetros
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
        return location.latitude, location.longitude

    @classmethod
    def marcado(cls, CERCAN, refe):
        cerca = []
        principalla, principallon = cls.traducir_coordenadas(refe)
        refeb = cls.obtener_direccion(principalla, principallon)

        for elemento in CERCAN:
            acompla, acomplon = cls.traducir_coordenadas(elemento[0])
            element0b = cls.obtener_direccion(acompla, acomplon)
            dist = cls.calcular_distancia(principalla, principallon, acompla, acomplon)

            if dist < 2:  # Comprobando la distancia
                cerca.append(f"{elemento[0]} a {dist} Km")
                print(f"--> {refeb} está a {dist:.2f} Km de {element0b}")

        return "No hay más casas cercanas" if not cerca else cerca

class InterfazGrafica:
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.configurar_ventana()

    def configurar_ventana(self):
        self.ventana_principal.title("Ubicación y Mapa con Tkinter")
        self.ventana_principal.geometry("600x300")

        # Resto de la configuración de la interfaz gráfica aquí

    def buscar_direccion(self):
        direccion = self.entrada_direccion.get()  # Obtener la dirección del campo de entrada
        if direccion:
            try:
                # Utilizar la API de Nominatim para geocodificar la dirección
                url = f"https://nominatim.openstreetmap.org/search?format=json&q={direccion}"
                response = requests.get(url)
                data = response.json()
                if data:
                    latitud = data[0]['lat']
                    longitud = data[0]['lon']
                    self.mostrar_mapa(latitud, longitud)
                    self.etiqueta_ubicacion.config(text="Ubicación encontrada. Abriendo mapa...")
                else:
                    self.etiqueta_ubicacion.config(text="Dirección no encontrada.")
            except Exception as e:
                self.etiqueta_ubicacion.config(text=f"Error al buscar la dirección: {e}")
        else:
            self.etiqueta_ubicacion.config(text="Por favor, ingresa una dirección.")

    def mostrar_mapa(self, latitud, longitud):
        url_mapa = f"https://www.openstreetmap.org/?mlat={latitud}&mlon={longitud}#map=12/{latitud}/{longitud}"
        webbrowser.open(url_mapa)

    def iniciar(self):
        self.ventana_principal.mainloop()

# Crear una instancia de la interfaz gráfica y comenzar el bucle
if __name__ == "__main__":
    interfaz = InterfazGrafica()
    interfaz.iniciar()

