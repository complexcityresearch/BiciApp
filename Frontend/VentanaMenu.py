from tkinter import Menu

from Backend import Constantes
from Frontend.Ventana import Ventana
import customtkinter as tk

from Frontend.VentanaEstadisticas import VentanaEstadisticas
from Frontend.VentanaFiltrador import VentanaFiltrador
from Frontend.VentanaMapa import VentanaMapa
from Frontend.VentanaVoronoi import VentanaVoronoi


class VentanaMenu(Ventana):

    def __init__(self,soluciones:dict,matrices:dict):
        super().__init__("Command center")
        self.soluciones = soluciones
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

        cadena = "Summary of execution\n" \
            "Kilometers to pick a bicycle : " + str(self.soluciones[Constantes.KMS_COGER_BICI])+"\n" \
            "Kilometers to drop a bicycle : " + str(self.soluciones[Constantes.KMS_DEJAR_BICI])+"\n" \
            "Unreal kilometers to pick a bicycle : " + str(self.soluciones[Constantes.KMS_FICTICIOS_COGER])+"\n" \
            "Unreal kilometers to drop a bicycle : " + str(self.soluciones[Constantes.KMS_FICTICIOS_DEJAR]) + "\n" \
            "Solved Petitions to pick a bicycle : " + str(self.soluciones[Constantes.PETICIONES_RESUELTAS_COGER_BICI]) + "\n" \
            "Solved Petitions to drop a bicycle : " + str(self.soluciones[Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI])+ "\n" \
            "Not solved Petitions to pick a bicycle : " + str(self.soluciones[Constantes.PETICIONES_NORESUELTAS_COGER_BICI] )+ "\n" \
            "Not solved Petitions to drop a bicycle : " + str(self.soluciones[Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI]) + "\n" \
            "Not solved unreal petitions to pick a bicycle : " + str(self.soluciones[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI]) + "\n" \
            "Not solved unreal petitions to drop a bicycle : " + str(self.soluciones[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI]) + "\n"
        texto = tk.CTkLabel(
        master = ventana,
        text = cadena,
        font = ("Arial",20),
        justify = tk.LEFT)

        texto.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

    def __menu(self,ventana):
        menubar = Menu(ventana)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=ventana.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        mapas_menu = Menu(menubar, tearoff=0)
        mapas_menu.add_command(label="Heat Map", command=lambda:self.__abrirVentanaMapa())
        mapas_menu.add_command(label="Voronoi Map", command=lambda:self.__abrirVentanaVoronoi())

        filtrado_menu = Menu(menubar,tearoff=0)
        filtrado_menu.add_command(label="Filter", command=lambda:self.__abrirVentanaFiltrado())

        estadisticas_menu = Menu(menubar,tearoff=0)
        estadisticas_menu.add_command(label="Statistics", command=lambda:self.__abrirVentenaEstadistica())

        menubar.add_cascade(label="Statistics",menu=estadisticas_menu)
        menubar.add_cascade(label="Maps", menu=mapas_menu)
        menubar.add_cascade(label="Handlers",menu=filtrado_menu)
        ventana.config(menu=menubar)

    def __abrirVentanaMapa(self):
        VentanaMapa(self.matrices)

    def __abrirVentanaFiltrado(self):
        VentanaFiltrador(self.matrices)

    def __abrirVentanaVoronoi(self):
        VentanaVoronoi(self.matrices)

    def __abrirVentenaEstadistica(self):
        VentanaEstadisticas(self.matrices)

def donothing():
    x=0