import tkinter as tk
from tkinter import ttk
import webbrowser
from gestor_ubicaciones import GestorUbicaciones
from casas import casas

class InterfazGUI:
    def __init__(self):
        self.gestor_ubicaciones = GestorUbicaciones() 
        self.ventana_principal = tk.Tk()

        self.ventana_principal.configure(bg='#7D3C98')
        self.configurar_ventana()

    def configurar_ventana(self):


        frame_principal = tk.Frame(self.ventana_principal, bg='#7D3C98', bd=2, relief=tk.FLAT)
        frame_principal.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        self.ventana_principal.columnconfigure(0, weight=1)
        self.ventana_principal.rowconfigure(0, weight=1)

        titulo = tk.Label(frame_principal, text="Casas para perezosos", font=("Arial", 16, "bold"), bg="#f0f0f0")
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
        ventana_direcciones.geometry("600x400") 

        tree = ttk.Treeview(ventana_direcciones, columns=('Dirección', 'Acción'), show='headings', height=20)
        tree.heading('Dirección', text='Dirección')
        tree.heading('Acción', text='Acción')
        # tree.heading('Acción2', text='Acción2')
        tree.column('Dirección', width=400)
        tree.column('Acción', width=100, anchor='center')
        # tree.column('Accion2', width=100, anchor='center')
        scrollbar = tk.Scrollbar(ventana_direcciones, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        if direcciones and direcciones != "No hay más casas cercanas":
            for direccion in direcciones:
                tree.insert('', tk.END, values=(direccion, 'Compra'))
        else:
            tree.insert('', tk.END, values=("No se encontraron direcciones cercanas.", ''))
        tree.bind('<Double-1>', lambda event: self.abrir_pasarela_pago(event, tree))


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

    def abrir_pasarela_pago(self, event, tree):
        item = tree.selection()[0]
        direccion = tree.item(item, 'values')[0] 
        
        if tree.identify_column(event.x) == '#2':
            ventana_pago = tk.Toplevel(self.ventana_principal)
            ventana_pago.title("Pasarela de Pago")
            ventana_pago.geometry("400x300")  
            
            tk.Label(ventana_pago, text="Correo:").grid(row=0, column=0, sticky='w', padx=10, pady=2)
            correo_entry = tk.Entry(ventana_pago)
            correo_entry.grid(row=0, column=1, sticky='e', padx=10, pady=2)
            
            tk.Label(ventana_pago, text="Cédula:").grid(row=1, column=0, sticky='w', padx=10, pady=2)
            cedula_entry = tk.Entry(ventana_pago)
            cedula_entry.grid(row=1, column=1, sticky='e', padx=10, pady=2)
            
            tk.Label(ventana_pago, text="Nombre:").grid(row=2, column=0, sticky='w', padx=10, pady=2)
            nombre_entry = tk.Entry(ventana_pago)
            nombre_entry.grid(row=2, column=1, sticky='e', padx=10, pady=2)
            
            tk.Label(ventana_pago, text="Método de pago:").grid(row=3, column=0, sticky='w', padx=10, pady=2)
            metodo_pago = tk.StringVar()
            metodo_pago_combobox = ttk.Combobox(ventana_pago, textvariable=metodo_pago, 
                                                values=["Tarjeta de crédito", "PayPal", "Transferencia bancaria"])
            metodo_pago_combobox.grid(row=3, column=1, sticky='e', padx=10, pady=2)
            
            tk.Label(ventana_pago, text="Número de Tarjeta:").grid(row=4, column=0, sticky='w', padx=10, pady=2)
            numero_tarjeta_entry = tk.Entry(ventana_pago)
            numero_tarjeta_entry.grid(row=4, column=1, sticky='e', padx=10, pady=2)
            numero_tarjeta_entry.grid_remove() 
            
            def on_metodo_pago_changed(event):
                if metodo_pago.get() == "Tarjeta de crédito":
                    numero_tarjeta_entry.grid()  
                else:
                    numero_tarjeta_entry.grid_remove() 

            metodo_pago_combobox.bind('<<ComboboxSelected>>', on_metodo_pago_changed)
            
            boton_continuar = tk.Button(ventana_pago, text="Continuar", command=lambda: mostrar_info_usuario())
            boton_continuar.grid(row=5, column=0, columnspan=2, pady=10)

            def mostrar_info_usuario():
                correo = correo_entry.get()
                cedula = cedula_entry.get()
                nombre = nombre_entry.get()
                metodo_pago_seleccionado = metodo_pago.get()
                numero_tarjeta = numero_tarjeta_entry.get() if metodo_pago_seleccionado == "Tarjeta de crédito" else "N/A"
                
                ventana_info = tk.Toplevel(ventana_pago)
                ventana_info.title("Información de Compra")
                ventana_info.geometry("400x250")
                
                info_text = f"Dirección: {direccion}\nCorreo: {correo}\nCédula: {cedula}\nNombre: {nombre}\nMétodo de Pago: {metodo_pago_seleccionado}\nNúmero de Tarjeta: {numero_tarjeta}"
                tk.Label(ventana_info, text=info_text).pack(padx=10, pady=10)
                
                boton_confirmar = tk.Button(ventana_info, text="Confirmar", command=confirmar_compra)
                boton_confirmar.pack(pady=10)

                def confirmar_compra():
                    ventana_confirmacion = tk.Toplevel(ventana_info)
                    ventana_confirmacion.title("Compra Realizada")
                    ventana_confirmacion.geometry("300x150")
                    tk.Label(ventana_confirmacion, text="Compra realizada con éxito.", font=("Arial", 14)).pack(pady=20)