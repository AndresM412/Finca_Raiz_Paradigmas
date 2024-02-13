import tkinter as tk
from tkinter import ttk
import webbrowser
from gestor_ubicaciones import GestorUbicaciones
from casas import casas

class InterfazGUI:
    def __init__(self):
        self.gestor_ubicaciones = GestorUbicaciones() 
        self.ventana_principal = tk.Tk()
        self.configurar_ventana()

    def configurar_ventana(self):
        self.ventana_principal.title("Ubicación y Mapa con Tkinter")
        self.ventana_principal.geometry("450x400")

        frame_principal = tk.Frame(self.ventana_principal, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        titulo = tk.Label(frame_principal, text="Ubicación y Mapa con Tkinter", font=("Arial", 16, "bold"), bg="#f0f0f0")
        titulo.grid(row=0, column=0, columnspan=2, pady=(0,20))

        etiqueta_instruccion = tk.Label(frame_principal, text="Ingresa tu dirección y presiona 'Buscar':", font=("Arial", 12), bg="#f0f0f0")
        etiqueta_instruccion.grid(row=1, column=0, sticky="w", pady=5)

        self.entrada_direccion = tk.Entry(frame_principal, width=50, font=("Arial", 10))
        self.entrada_direccion.grid(row=2, column=0, pady=5, sticky="we")

        boton_buscar_direccion = tk.Button(frame_principal, text="Buscar", command=self.buscar_direccion, relief="groove", bg="#4CAF50", fg="white")
        boton_buscar_direccion.grid(row=2, column=1, padx=10, pady=5)

        self.etiqueta_ubicacion = tk.Label(frame_principal, text="", font=("Arial", 10), bg="#f0f0f0")
        self.etiqueta_ubicacion.grid(row=3, column=0, columnspan=2, pady=10)

        boton_buscar_cercanas = tk.Button(frame_principal, text="Buscar Direcciones Cercanas", command=self.mostrar_direcciones_cercanas, relief="groove", bg="#008CBA", fg="white")
        boton_buscar_cercanas.grid(row=4, column=0, columnspan=2, pady=10)
       
    def mostrar_direcciones_cercanas(self):
        direccion_referencia = self.entrada_direccion.get()
        if direccion_referencia:
            direcciones_cercanas = self.gestor_ubicaciones.marcado(direccion_referencia)
            self.abrir_ventana_direcciones(direcciones_cercanas)
        else:
            self.etiqueta_ubicacion.config(text="Por favor, ingresa una dirección de referencia.")

    def abrir_ventana_direcciones(self, direcciones):
        ventana_direcciones = tk.Toplevel(self.ventana_principal)
        ventana_direcciones.title("Direcciones Cercanas")
        ventana_direcciones.geometry("500x300")
        texto_direcciones = "\n".join(direcciones) if direcciones else "No se encontraron direcciones cercanas."
        tk.Label(ventana_direcciones, text=texto_direcciones, justify=tk.LEFT).pack(pady=10, padx=10)

    def buscar_direccion(self):
        direccion = self.entrada_direccion.get() 
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