from Backend import Constantes
from Backend.GuardarCargarDatos import GuardarCargarMatrices
from Frontend.Ventana import Ventana
import customtkinter as tk

from Frontend.VentanaMenu import VentanaMenu

from bike_simulator5 import bike_simulator5


class VentanaPrincipal(Ventana):

    def __init__(self):
        super().__init__("Main window")
        self.directorios = [None] * 6
        ventana = super().getVentanaAttribute()

        self.textoDelta = tk.CTkTextbox(master=ventana, height=10)
        self.textoCapacidad = tk.CTkTextbox(master=ventana, height=10)
        self.textoCercanasIndices = tk.CTkTextbox(master=ventana, height=10)
        self.textoCercanasKms = tk.CTkTextbox(master=ventana, height=10)
        self.textoCoordenadas = tk.CTkTextbox(master=ventana, height=10)
        self.textbox_deltaTime = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textoTendencias = tk.CTkTextbox(master=ventana, height=10)
        self.textoMatrizCustom = tk.CTkTextbox(master=ventana, height=10)

        self.establecerDeltaTime(ventana)
        self.cargarTextoDatos()
        self.botonCargarDatos(ventana)
        self.titulo(ventana)
        self.textoExplicacion(ventana)
        super().ejecutarVentana()

    def cargarTextoDatos(self):
        self.textoDelta.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
        self.textoDelta.insert("0.0", "No file")

        self.textoCapacidad.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.textoCapacidad.insert("0.0", "No file")

        self.textoCercanasIndices.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
        self.textoCercanasIndices.insert("0.0", "No file")

        self.textoCercanasKms.place(relx=0.3, rely=0.7, anchor=tk.CENTER)
        self.textoCercanasKms.insert("0.0", "No file")

        self.textoCoordenadas.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
        self.textoCoordenadas.insert("0.0", "No file")

        self.textoTendencias.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
        self.textoTendencias.insert("0.0", "No file")

        self.textoMatrizCustom.place(relx=0.1, rely=0.8, anchor=tk.CENTER)
        self.textoMatrizCustom.insert("0.0","No file")

    def establecerDeltaTime(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Select the delta time:",
            font=("Arial", 20),
        )
        titulo.place(relx=0.8, rely=0.3)
        self.textbox_deltaTime.place(relx=0.8, rely=0.35)

    def botonCargarDatos(self, ventana):
        ##Boton deltas:
        boton_delta = tk.CTkButton(master=ventana, text="Load Delta File",
                                   command=lambda: self.__cargarFicheroDelta(ventana, 0))
        boton_delta.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        # Boton capacidades
        boton_capacidad = tk.CTkButton(master=ventana, text="Load File Capacity",
                                       command=lambda: self.__cargarFicheroDelta(ventana, 1))
        boton_capacidad.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

        # Boton cercanas_indices
        boton_cercanas_indices = tk.CTkButton(master=ventana, text="Load File Nearby_indices",
                                              command=lambda: self.__cargarFicheroDelta(ventana, 2))
        boton_cercanas_indices.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        # Boton cercanas_kms
        boton_cercanas_kms = tk.CTkButton(master=ventana, text="Load File Nearby_kms",
                                          command=lambda: self.__cargarFicheroDelta(ventana, 3))
        boton_cercanas_kms.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

        # Boton coordenadas
        boton_coordenadas = tk.CTkButton(master=ventana, text="Load Coordinates File",
                                         command=lambda: self.__cargarFicheroDelta(ventana, 4))
        boton_coordenadas.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
        # Boton tendencias

        boton_tendencias = tk.CTkButton(master=ventana, text="Upload file Trends",
                                        command=lambda: self.__cargarFicheroDelta(ventana, 5))
        boton_tendencias.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

        # Boton_enviar_datos
        boton_enviar_datos = tk.CTkButton(master=ventana, text="Review and Submit Data",
                                          command=lambda: self.__comprobarDatos(ventana))
        boton_enviar_datos.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        # Boton_enviar_datos
        boton_cargarDatos = tk.CTkButton(master=ventana, text="Take the data of the last execution",
                                          command=lambda: self.__boton_cargarDatos())
        boton_cargarDatos.place(relx=0.3, rely=0.95, anchor=tk.CENTER)

        #Boton cargar matriz custom
        boton_cargarDatos = tk.CTkButton(master=ventana, text="Load custom matrix",
                                         command=lambda: self.__cargarFicheroDelta(ventana, 6))
        boton_cargarDatos.place(relx=0.1, rely=0.95, anchor=tk.CENTER)


    def __boton_cargarDatos(self):
        matrices = GuardarCargarMatrices.cargarAntiguaEjecucion()
        self.__llamarVentanaMenu(matrices)

    def titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Data upload",
            font=("Arial", 70),
        )
        titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    def textoExplicacion(self, ventana):
        texto = tk.CTkLabel(
            master=ventana,
            text="Please enter the following data",
            font=("Arial", 20))

        texto.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

    def __cargarFicheroDelta(self, ventana, boton):

        directorio = tk.filedialog.askopenfilenames()
        print(directorio)
        listaTextos = [self.textoDelta, self.textoCapacidad, self.textoCercanasIndices, self.textoCercanasKms,
                       self.textoCoordenadas, self.textoTendencias,self.textoMatrizCustom]
        listaTextos[boton].delete("0.0", "end")
        listaTextos[boton].insert("0.0", directorio[0])
        self.directorios[boton] = directorio[0]
        listaTextos[boton].update()
        Constantes.DELTA_TIME = int(self.textbox_deltaTime.get("0.0", 'end-1c'))

    def __comprobarDatos(self, ventana):
        listaTextos = [self.textoDelta, self.textoCapacidad, self.textoCercanasIndices, self.textoCercanasKms,
                       self.textoCoordenadas, self.textoTendencias]
        listaRutas = []
        for texto in listaTextos:
            if not texto.get("0.0", "end").__contains__("No file"):
                listaRutas.append(texto.get("0.0", "end"))

        # Si falta algun fichero:
        if len(listaRutas) < 6 or self.textbox_deltaTime.get("0.0", 'end-1c') == "":
            dialog = tk.CTkInputDialog(text="ERROR: NOT ALL DATA ENTERED", title="ERROR")
            listaRutas.clear()
        else:
            bs = bike_simulator5()
            nearest_stations_idx, nearest_stations_distance, initial_movements, real_movements, capacidadInicial, coordenadas = bs.load_data(directorios=self.directorios)

            coste, matrices = bs.evaluate_solution(capacidadInicial, initial_movements, real_movements,
                                                   nearest_stations_idx, nearest_stations_distance)
            GuardarCargarMatrices.guardarArchivosEjecucion(matrices)
            self.__llamarVentanaMenu(matrices)





    def __llamarVentanaMenu(self,matrices):

        #Voy a ver si existe la matriz custom.
        if self.textoMatrizCustom.get("0.0", "end-1c") != "No file" and self.textoMatrizCustom.get("0.0", "end-1c") != "":
            Constantes.MATRIZ_CUSTOM = GuardarCargarMatrices.cargarMatrizCustom(self.textoMatrizCustom.get("0.0", "end-1c"))



        Kms_coger = matrices[Constantes.KMS_COGER_BICI].matrix.iloc[:, 1:].sum().sum()
        Kms_dejar = matrices[Constantes.KMS_DEJAR_BICI].matrix.iloc[:, 1:].sum().sum()

        Kms_ficticios_coger = matrices[Constantes.KMS_FICTICIOS_COGER].matrix.iloc[:, 1:].sum().sum()
        Kms_ficticios_dejar = matrices[Constantes.KMS_FICTICIOS_DEJAR].matrix.iloc[:, 1:].sum().sum()

        N_Peticiones_Resueltas_coger = matrices[Constantes.PETICIONES_RESUELTAS_COGER_BICI].matrix.iloc[:,
                                       1:].sum().sum()
        N_Peticiones_Resueltas_dejar = matrices[Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI].matrix.iloc[:,
                                       1:].sum().sum()

        N_Peticiones_noResueltas_coger = matrices[Constantes.PETICIONES_NORESUELTAS_COGER_BICI].matrix.iloc[:,
                                         1:].sum().sum()
        N_Peticiones_noResueltas_dejar = matrices[Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI].matrix.iloc[:,
                                         1:].sum().sum()

        N_Peticiones_Ficticias_noResueltas_coger = matrices[
                                                       Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI].matrix.iloc[
                                                   :, 1:].sum().sum()
        N_Peticiones_Ficticias_noResueltas_dejar = matrices[
                                                       Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI].matrix.iloc[
                                                   :, 1:].sum().sum()

        soluciones = {
            Constantes.KMS_COGER_BICI: Kms_coger,
            Constantes.KMS_DEJAR_BICI: Kms_dejar,
            Constantes.KMS_FICTICIOS_COGER: Kms_ficticios_coger,
            Constantes.KMS_FICTICIOS_DEJAR: Kms_ficticios_dejar,
            Constantes.PETICIONES_NORESUELTAS_COGER_BICI: N_Peticiones_noResueltas_coger,
            Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI: N_Peticiones_noResueltas_dejar,
            Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI: N_Peticiones_Ficticias_noResueltas_coger,
            Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI: N_Peticiones_Ficticias_noResueltas_dejar,
            Constantes.PETICIONES_RESUELTAS_COGER_BICI: N_Peticiones_Resueltas_coger,
            Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI: N_Peticiones_Resueltas_dejar

        }
        # End temporal

        matrices = VentanaMenu(soluciones=soluciones, matrices=matrices)


