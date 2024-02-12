# Crear la ventana principal de Tkinter y pasarla a la clase InterfazGUI
import prueba
import tkinter as tk


def main():
    root = tk.Tk()
    app = prueba.InterfazGUI()
    root.mainloop()

if __name__ == "__main__":
    main()
