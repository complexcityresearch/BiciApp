from Backend import Constantes

from Backend.GuardarCargarDatos import GuardarCargarMatrices
from Frontend.Ventana import Ventana
import customtkinter as tk

from Frontend.VentanaAnalizador import VentanaAnalizador
from Frontend.VentanaGeneradorEstadistico import VentanaGeneradorEstadistico
from Frontend.VentanaSimulador import VentanaSimulador


class VentanaSeleccionHerramienta(Ventana):

    def __init__(self):
        super().__init__("Tool Selection")
        ventana = super().getVentanaAttribute()
        self.titulo(ventana)
        self.definirBotones(ventana)
        super().ejecutarVentana()

    def titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Tool Selection",
            font=("Arial", 70),
        )
        titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    def definirBotones(self,ventana):
        boton_simular = tk.CTkButton(master=ventana, text="Simulate",
                                   command=self.seleccionarSimular)
        boton_simular.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        boton_analizar = tk.CTkButton(master=ventana, text="Analyze",
                                   command=self.seleccionarAnalizar)
        boton_analizar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        boton_generador = tk.CTkButton(master=ventana, text="Generate Data",
                                      command=self.seleccionarGenerar)
        boton_generador.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


    def seleccionarSimular(self):
        VentanaSimulador()

    def seleccionarAnalizar(self):
        directorio = tk.filedialog.askdirectory()
        nombreDirectorio = directorio.split('/')[-1]
        matrices,resumentxt = GuardarCargarMatrices.cargarSimulacionesParaAnalisis(directorio)
        Constantes.DELTA_TIME = float(resumentxt[0])
        Constantes.PORCENTAJE_ESTRES = float(resumentxt[1])
        Constantes.COSTE_ANDAR = float(resumentxt[2])
        VentanaAnalizador(matrices,resumentxt,nombreDirectorio)

    def seleccionarGenerar(self):
        VentanaGeneradorEstadistico()