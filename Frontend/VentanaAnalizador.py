from tkinter import Menu

from Backend import Constantes

from Frontend.Ventana import Ventana
import customtkinter as tk

from Frontend.VentanaDesplazamientos import VentanaDesplazamientos

from Frontend.VentanaEstadisticas2 import VentanaEstadisticas2

from Frontend.VentanaFiltrador2 import VentanaFiltrador2

from Frontend.VentanaMapa2 import VentanaMapa2



class VentanaAnalizador(Ventana):

    def __init__(self,matrices:dict,resumen:list[str],nombreDirectorio:str):
        super().__init__("Analyzer")
        self.nombreDirectorio=nombreDirectorio
        self.resumentxt = resumen
        self.matrices = matrices
        ventana = super().getVentanaAttribute()
        self.__titulo(ventana)
        self.__ResumenEjecucion(ventana)
        self.__menu(ventana)
        super().ejecutarVentana()

    def __titulo(self,ventana):
        titulo = tk.CTkLabel(
            master = ventana,
            text = "Control center",
            font=("Arial",70),
        )
        titulo.place(relx=0.5,rely=0.2,anchor=tk.CENTER)

    def __ResumenEjecucion(self,ventana):

        intro = "Representing a summary of the directory execution: " + self.nombreDirectorio

        texto_introduccion = tk.CTkLabel(
            master=ventana,
            text=intro,
            font=("Arial", 30),
            justify=tk.LEFT)
        texto_introduccion.place(relx=0.5,rely=0.3,anchor=tk.CENTER)



        cadena = self.__parsearResumen(self.resumentxt)

        texto = tk.CTkLabel(
        master = ventana,
        text = cadena,
            font=("Courier", 20),
            justify="left",
            padx=10)

        texto.place(relx=0.5,rely=0.6,anchor=tk.CENTER)

    def __parsearResumen(self, texto: list[str]):
        # Convertir todos los valores a float
        try:
            valores = [float(valor.replace(",", ".")) for valor in texto]  
        except ValueError:
            return "Error: Some values are not numbers."

        # Definir las etiquetas
        etiquetas = [
            "Deltas",
            "Stress",
            "Kilometers to pick a bicycle",
            "Kilometers to drop a bicycle",
            "Unreal km to pick a bicycle",
            "Unreal km to drop a bicycle",
            "Solved petitions to pick",
            "Solved petitions to drop",
            "Not solved petitions to pick",
            "Not solved petitions to drop",
            "Solved unreal petitions to pick",
            "Solved unreal petitions to drop",
            "Not solved unreal petitions to pick",
            "Not solved unreal petitions to drop"
        ]

        # Formatear en columnas
        cadena = "Data Summary:\n"
        cadena += "-" * 50 + "\n"

        for etiqueta, valor in zip(etiquetas, valores):
            cadena += f"{etiqueta:<40} {valor:>10.2f}\n" 

        return cadena


    def __menu(self,ventana):
        menubar = Menu(ventana)

        mapas_menu = Menu(menubar, tearoff=0)
        mapas_menu.add_command(label="Density, Voronoi and Circle Maps", command=self.__abrirVentanaMapa)
        mapas_menu.add_command(label="Map Displacements", command=self.__abrirVentanaDesplazamientos)

        filtrado_menu = Menu(menubar,tearoff=0)
        filtrado_menu.add_command(label="Filter", command=self.__abrirVentanaFiltrado)

        estadisticas_menu = Menu(menubar,tearoff=0)
        estadisticas_menu.add_command(label="Statistics", command=self.__abrirVentenaEstadistica)

        menubar.add_cascade(label="Statistics",menu=estadisticas_menu)
        menubar.add_cascade(label="Maps", menu=mapas_menu)
        menubar.add_cascade(label="Filters",menu=filtrado_menu)
        ventana.config(menu=menubar)

    def __abrirVentanaMapa(self):
        VentanaMapa2(self.matrices)

    def __abrirVentanaFiltrado(self):
        VentanaFiltrador2(self.matrices)

    def __abrirVentanaDesplazamientos(self):
        VentanaDesplazamientos(self.matrices[Constantes.DESPLAZAMIENTOS].matrix)

    def __abrirVentenaEstadistica(self):
        VentanaEstadisticas2(self.matrices)