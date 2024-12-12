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

    def __parsearResumen(self,texto:list[str]):

        cadena = "Deltas : \t\t\t\t\t" + texto[0] + "\n" + \
         "Stress: \t\t\t\t\t" + texto[1] + "\n" +\
         "Kms Reales coger: \t\t\t\t" + texto[2] + "\n" +\
         "Kms Reales soltar: \t\t\t\t" + texto[3] + "\n" +\
         "Kms Ficticios coger: \t\t\t\t" + texto[4] + "\n" +\
         "Kms Ficticios soltar: \t\t\t\t" + texto[5] + "\n" +\
         "Peticiones Reales resueltas coger: \t\t" + texto[6] + "\n" +\
         "Peticiones Reales resueltas soltar: \t\t" + texto[7] + "\n" +\
         "Peticiones Reales no resueltas coger: \t\t" + texto[8] + "\n" +\
         "Peticiones Reales no resueltas soltar: \t\t" + texto[9] + "\n" +\
         "Peticiones Ficticias resueltas coger: \t\t" + texto[10] + "\n" +\
         "Peticiones Ficticias resueltas soltar: \t\t" + texto[11] + "\n" +\
         "Peticiones Ficticias no resueltas coger: \t" + texto[12] + "\n" +\
         "Peticiones Ficticias no resueltas soltar: \t" + texto[13]
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