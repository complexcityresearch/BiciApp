from os.path import join

import pandas as pd

from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros, Extractor
from Backend.GuardarCargarDatos import GuardarCargarMatrices
from Frontend.Ventana import Ventana
import customtkinter as tk
from bike_simulator5 import bike_simulator5


class VentanaSimulador(Ventana):

    def __init__(self):
        super().__init__("Simulator")

        ventana = super().getVentanaAttribute()
        self.ventana = ventana # Temporal fix to show text. Pending to general fix.
        self.titulo(ventana)
        self.directorioEntrada = ""
        self.directorioSalida = ""
        self.opcion_var = tk.StringVar()
        self.texbox_delta = tk.CTkTextbox(master=ventana, height=10)
        self.texbox_stress = tk.CTkTextbox(master=ventana, height=10)
        self.texbox_stress_estaciones = tk.CTkTextbox(master=ventana, height=10)
        self.texbox_tipoStress = tk.CTkTextbox(master=ventana, height=10)
        self.texbox_costeAndar = tk.CTkTextbox(master=ventana, height=10)
        self.textbox_extraerDias = tk.CTkTextbox(master=ventana, height=10)
        self.textoExplicacion(ventana)
        
        super().ejecutarVentana()

    def titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Simulator",
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
            text="Delta_Time :",
            font=("Arial", 10))
        texto_delta.place(relx=0.2, rely=0.6, anchor=tk.CENTER)
        self.texbox_delta.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
        self.texbox_delta.insert("0.0", "15")
        texto_stress = tk.CTkLabel(
            master=ventana,
            text="Stress :",
            font=("Arial", 10))
        texto_stress.place(relx=0.7, rely=0.6, anchor=tk.CENTER)
        self.texbox_stress.place(relx=0.8, rely=0.6, anchor=tk.CENTER)
        self.texbox_stress.insert("0.0", "0")
        texto_tipoStress = tk.CTkLabel(
            master=ventana,
            text="Stress Type :",
            font=("Arial", 10))
        texto_tipoStress.place(relx=0.2, rely=0.7, anchor=tk.CENTER)
        #self.texbox_tipoStress.place(relx=0.3, rely=0.7, anchor=tk.CENTER)



        # Crear los radio buttons
        radiobutton_1 = tk.CTkRadioButton(master=ventana, text="Bicycle Stressing",
                                                      variable=self.opcion_var, value=1)
        radiobutton_2 = tk.CTkRadioButton(master=ventana, text="Stress Requests",
                                          variable=self.opcion_var, value=2)
        radiobutton_3 = tk.CTkRadioButton(master=ventana, text="Stress Everything",
                                          variable=self.opcion_var, value=3)
        radiobutton_4 = tk.CTkRadioButton(master=ventana, text="No Stress",
                                          variable=self.opcion_var, value="")#For no stressing.
        radiobutton_1.place(relx=0.25,rely=0.7)
        radiobutton_2.place(relx=0.35, rely=0.7)
        radiobutton_3.place(relx=0.45, rely=0.7)
        radiobutton_4.place(relx=0.55, rely= 0.7)

        texto_estacionesStress = tk.CTkLabel(
            master=ventana,
            text="Apply to Stations:",
            font=("Arial", 10))
        texto_estacionesStress.place(relx=0.7, rely=0.7, anchor=tk.CENTER)
        self.texbox_stress_estaciones.place(relx=0.8, rely=0.7, anchor=tk.CENTER)
        self.texbox_stress_estaciones.insert("0.0", "All")

        texto_costeAndar = tk.CTkLabel(
            master=ventana,
            text="Cost of walking :",
            font=("Arial", 10))
        texto_costeAndar.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.texbox_costeAndar.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
        self.texbox_costeAndar.insert("0.0", "1")


        texto_extraerDias = tk.CTkLabel(
            master=ventana,
            text="Extract Days :",
            font=("Arial", 10))
        texto_extraerDias.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
        self.textbox_extraerDias.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        self.textbox_extraerDias.insert("0.0", "_")

        self.boton_RealizarSimulacion = tk.CTkButton(master=ventana, text="Perform Simulation",
                                          command=self.realizarSimulacion)
        self.boton_RealizarSimulacion.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def cargarDirectorioEntrada(self):

        directorio = tk.filedialog.askdirectory()
        self.directorioEntrada = directorio
        texto_ruta = tk.CTkLabel(
            master=self.ventana,
            text=directorio,
            font=("Arial", 10))
        texto_ruta.place(relx=0.4, rely=0.45, anchor=tk.CENTER)

    def cargarDirectorioSalida(self):

        directorio = tk.filedialog.askdirectory()
        self.directorioSalida = directorio
        texto_ruta = tk.CTkLabel(
            master=self.ventana,
            text=directorio,
            font=("Arial", 10))
        texto_ruta.place(relx=0.6, rely=0.45, anchor=tk.CENTER)

    def realizarSimulacion(self):
        color_original = self.boton_RealizarSimulacion.cget("fg_color")
        self.boton_RealizarSimulacion.configure(fg_color="grey")
        self.ventana.update_idletasks()  # FORZA actualización de la interfaz

        rutaEntrada = self.directorioEntrada
        rutaSalida = self.directorioSalida
        delta = float(self.texbox_delta.get("0.0", "end-1c"))
        coste_andar = float(self.texbox_costeAndar.get("0.0", "end-1c"))

        stress = self.texbox_stress.get("0.0", "end-1c")
        estacionesStress = self.texbox_stress_estaciones.get("0.0", "end-1c")#Parsear esto.
        tipoStress = self.texbox_tipoStress.get("0.0", "end-1c")
        extraerDias = self.textbox_extraerDias.get("0.0", "end-1c")  # Parsear esto.

        if estacionesStress != 'All':
            estacionesStress = list(map(int, estacionesStress.split(',')))


        ficheros,ficheros_distancia = GuardarCargarMatrices.cargarDatosParaSimular(rutaEntrada)
        Constantes.DELTA_TIME = delta
        Constantes.COSTE_ANDAR = coste_andar
        Constantes.PORCENTAJE_ESTRES = stress

        if extraerDias != '_':  # Extraer dias es optativo.
            dias = list(map(int, extraerDias.split(",")))
            path_fichero = join(rutaSalida, auxiliar_ficheros.formatoArchivo("Extraccion_" + str(dias), "csv"))
            Extractor.extraerDias(ficheros[0], delta, dias, path_fichero, mantenerPrimeraFila=True)
            ficheros[0] = path_fichero

        # Intercambio los deltas con el stress.
        if stress != '' and stress != '0' and self.opcion_var.get() != "":
            stress = float(stress)

            ficheroDelta_salidaStress = join(rutaSalida, auxiliar_ficheros.formatoArchivo("Dstress", "csv"))
            Extractor.extraerStressAplicado(ficheros[0], ficheroDelta_salidaStress, stress, tipoStress=int(self.opcion_var.get()),
                                            listaEstaciones=estacionesStress)

            ficheroTendencias_salidaStress = join(rutaSalida,
                                                  auxiliar_ficheros.formatoArchivo("Tendencias_stress", "csv"))
            Extractor.extraerStressAplicado(ficheros[5], ficheroTendencias_salidaStress, stress,
                                            tipoStress=int(self.opcion_var.get()), listaEstaciones=estacionesStress)

            ficheros[0] = ficheroDelta_salidaStress
            ficheros[5] = ficheroTendencias_salidaStress

        bs = bike_simulator5()
        nearest_stations_idx, nearest_stations_distance, initial_movements, real_movements, capacidadInicial, coordenadas = bs.load_data(
            directorios=ficheros, directorios_DiastanciasAndarBicicleta=ficheros_distancia)
        coste, matricesSalida = bs.evaluate_solution(capacidadInicial, initial_movements, real_movements,
                                                     nearest_stations_idx, nearest_stations_distance)
        resumen = auxiliar_ficheros.hacerResumenMatricesSalida(matricesSalida)

        auxiliar_ficheros.guardarMatricesEnFicheros(matricesSalida, resumen, rutaSalida)
        pd.DataFrame(Constantes.COORDENADAS).to_csv(join(rutaSalida, "coordenadas" + ".csv"), index=False)
        archivoCapacidad = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["capacidades"])[0]
        pd.read_csv(archivoCapacidad).transpose().to_csv(join(rutaSalida,"capacidades.csv"), index=False)
        self.boton_RealizarSimulacion.configure(fg_color= color_original)