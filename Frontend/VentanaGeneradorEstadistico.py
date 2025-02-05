from os.path import join

import pandas as pd

from Backend.Auxiliares import auxiliar_ficheros
from Backend.OperacionesDeltas.SimuladorDeltasEstadistico import SimuladorDeltasEstadistico
from Frontend.Ventana import Ventana
import customtkinter as tk

class VentanaGeneradorEstadistico(Ventana):

    def __init__(self):
        super().__init__("Statistical generator")

        ventana = super().getVentanaAttribute()
        self.titulo(ventana)
        self.directorioEntrada = ""
        self.directorioSalida = ""
        self.texbox_delta = tk.CTkTextbox(master=ventana, height=10)
        self.texbox_dias = tk.CTkTextbox(master=ventana, height=10)
        self.opciones = ["Added","Natural"]
        self.combobox = tk.CTkOptionMenu(master=ventana,
                                         values=self.opciones,

                                         )
        self.combobox.place(relx=0.6, rely=0.6)
        self.textoExplicacion(ventana)
        super().ejecutarVentana()

    def titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Statistical generator",
            font=("Arial", 70),
        )
        titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    def textoExplicacion(self, ventana):
        texto = tk.CTkLabel(
            master=ventana,
            text="Enter the input and output directories",
            font=("Arial", 20))

        texto.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        boton_datosEntrada = tk.CTkButton(master=ventana, text="Load Directory Input data",
                                         command=self.cargarDirectorioEntrada)
        boton_datosEntrada.place(relx=0.4, rely=0.4, anchor=tk.CENTER)

        boton_datosSalida = tk.CTkButton(master=ventana, text="Load Directory Output data",
                                         command=self.cargarDirectorioSalida)
        boton_datosSalida.place(relx=0.6, rely=0.4, anchor=tk.CENTER)


        texto_parametros = tk.CTkLabel(
            master=ventana,
            text="Enter the parameters required for the simulation:",
            font=("Arial", 20))
        texto_parametros.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        texto_delta = tk.CTkLabel(
            master=ventana,
            text="Actual Delta_Time:",
            font=("Arial", 10))
        texto_delta.place(relx=0.2, rely=0.6, anchor=tk.CENTER)
        self.texbox_delta.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        texto_dias = tk.CTkLabel(
            master=ventana,
            text="Days to simulate :",
            font=("Arial", 10))
        texto_dias.place(relx=0.2, rely=0.7, anchor=tk.CENTER)
        self.texbox_dias.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        boton_RealizarSimulacion = tk.CTkButton(master=ventana, text="Statistical generation",
                                                command=self.realizarGeneracion)
        boton_RealizarSimulacion.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        texto_ruleta = tk.CTkLabel(
            master=ventana,
            text="Select the generation method :",
            font=("Arial", 10))
        texto_ruleta.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


    def cargarDirectorioEntrada(self):

        directorio = tk.filedialog.askdirectory()
        print(directorio)
        self.directorioEntrada = directorio

    def cargarDirectorioSalida(self):

        directorio = tk.filedialog.askdirectory()
        print(directorio)
        self.directorioSalida = directorio


    def realizarGeneracion(self):

        rutaDeltas = auxiliar_ficheros.buscar_archivosEntrada(self.directorioEntrada, ['deltas','Extraccion'])
        deltaActual = self.texbox_delta.get("0.0", "end-1c")
        matrizDeltas = pd.read_csv(rutaDeltas[0])
        diasSimular = self.texbox_dias.get("0.0", "end-1c")
        simuladorDE = SimuladorDeltasEstadistico(matrizDeltas, int(deltaActual))

        if self.combobox.get() == self.opciones[0]:
            nuevoFicheroDeltas = simuladorDE.simularDatosEstadisticos_PeriodoTotal(int(diasSimular))
        else:
            dias = list(range(0, int(diasSimular)))
            nuevoFicheroDeltas = simuladorDE.simularDatosEstadisticos_Horas(dias)


        nombre = auxiliar_ficheros.formatoArchivo("deltasGeneradosEstadistica", "csv")
        nuevoFicheroDeltas.to_csv(join(self.directorioSalida,nombre), index=False)
