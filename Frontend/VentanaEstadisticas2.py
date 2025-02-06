

from Backend import Constantes
from Backend.Auxiliares import auxiliaresCalculos
from Backend.Manipuladores import Agrupador

from Backend.estadisticasOcupacionHorarias import estadisticasOcupacionHorarias
from Frontend.Ventana import Ventana
import customtkinter as tk
import tkinter as tt
from tkinter import ttk, messagebox


class VentanaEstadisticas2(Ventana):

    def __init__(self, matrices: dict):
        super().__init__("Statistics Generator")
        self.matrices = matrices
        self.listaMatrices = []
        self.checkmatrizCustom = None
        ventana = super().getVentanaAttribute()
        self.delta_media = tk.BooleanVar()
        self.textbox_deltasActuales = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_deltasTransformar = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_dias = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_estacion = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.combobox = tk.CTkOptionMenu(master=ventana,
                                         values=["Accumulated graph of a station",
                                                 "Average graph of a station",
                                                 "Bar graph Average of all stations",
                                                 "Graph comparing stations",
                                                 "Graph comparing matrices",
                                                 ],
                                         command=self.seleccionarGrafico,
                                         )
        self.__seleccionarEstadisticas()
        self.textbox_deltaCustom = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_diasCustom = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_estacionesCustom = tk.CTkTextbox(master=ventana, height=5, width=135)

        self.labels_titulos = {}
        self.__cargarLabels(ventana)
        self.frecuencia = tk.BooleanVar()
        self.check_frecuencia = tk.CTkCheckBox(ventana, text="Represent Frequency?", variable=self.frecuencia)
        self.histogramaMediaAcumulada = tk.BooleanVar()
        self.check_histogramaMediaAcumulada = tk.CTkCheckBox(ventana, text="Represent by Media?",
                                                             variable=self.histogramaMediaAcumulada)

        self.__titulo(ventana)
        self.__seleccionMatrices(ventana)
        self.__boton(ventana)
        self.__mostrarSeleccionEstacionDias()

        self.__cambiarDeltas(ventana)
        super().ejecutarVentana()

    def __titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Statistics",
            font=("Arial", 70),
        )
        descripcion = tk.CTkLabel(
            master=ventana,
            text="Matrices to be represented",
            font=("Arial", 20),
        )
        # titulo.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        titulo.pack()
        descripcion.pack(side=tk.TOP, pady=5, padx=1, anchor="w")

    def __cargarLabels(self, ventana):
        self.labels_titulos['seleccionHistogramaDiario'] = tk.CTkLabel(
            master=ventana,
            text="Select the days, the grouping method and the desired frequency:",
            font=("Arial", 20),
        )

        self.labels_titulos['seleccionEstacionDias'] = tk.CTkLabel(
            master=ventana,
            text="Select the station and days:",
            font=("Arial", 20),
        )

        self.labels_titulos['seleccionGraficaComparacionEstaciones'] = tk.CTkLabel(
            master=ventana,
            text="Select the stations to be compared and the days of these stations",
            font=("Arial", 20),
        )

        self.labels_titulos['seleccionGraficaComparacionMatrices'] = tk.CTkLabel(
            master=ventana,
            text="Select the stations to be compared and the days of these stations",
            font=("Arial", 20),
        )

        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMA'] = tk.CTkLabel(
            master=ventana,
            text="Stations of the current matrix:",
            font=("Arial", 15),
        )
        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMC'] = tk.CTkLabel(
            master=ventana,
            text="Custom matrix stations:",
            font=("Arial", 15),
        )
        self.labels_titulos['seleccionGraficaComparacionMatricesDeltaMC'] = tk.CTkLabel(
            master=ventana,
            text="Delta of the Custom matrix:",
            font=("Arial", 15),
        )

    def __boton(self, ventana):


        boton = tk.CTkButton(master=ventana, text="Generate Statistics",
                             command=lambda: self.__getBotonesPulsados())

        boton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)


    def __seleccionMatrices(self, ventana):
        check_ocupacion = tk.BooleanVar()
        check_kms_coger = tk.BooleanVar()
        check_kms_dejar = tk.BooleanVar()
        check_peticionesResueltas_coger = tk.BooleanVar()
        check_peticionesResueltas_dejar = tk.BooleanVar()
        check_peticionesNoResueltas_coger = tk.BooleanVar()
        check_peticionesNoResueltas_dejar = tk.BooleanVar()
        check_ocupacionRelativa = tk.BooleanVar()
        check_kmsFicticios_coger = tk.BooleanVar()
        check_kmsFicticios_dejar = tk.BooleanVar()
        check_NoResueltas_ficticias_coger = tk.BooleanVar()
        check_NoResueltas_ficticias_dejar = tk.BooleanVar()
        check_Matriz_Custom = tk.BooleanVar()
        check_peticionesResueltas_ficticias_coger = tk.BooleanVar()
        check_peticionesResueltas_ficticias_dejar = tk.BooleanVar()

        self.checkmatrizCustom = check_Matriz_Custom

        self.listaMatrices = [check_ocupacion,
                              check_ocupacionRelativa,
                              check_kms_coger,
                              check_kms_dejar,
                              check_peticionesResueltas_coger,
                              check_peticionesResueltas_dejar,
                              check_peticionesNoResueltas_coger,
                              check_peticionesNoResueltas_dejar,
                              check_kmsFicticios_coger,
                              check_kmsFicticios_dejar,
                              check_peticionesResueltas_ficticias_coger,
                              check_peticionesResueltas_ficticias_dejar,
                              check_NoResueltas_ficticias_coger,
                              check_NoResueltas_ficticias_dejar,

                              ]

        # Creamos el checkbox

        check_button1 = tk.CTkCheckBox(ventana, text="Occupancy", variable=check_ocupacion)
        check_button2 = tk.CTkCheckBox(ventana, text="Relative Occupancy", variable=check_ocupacionRelativa)
        check_button3 = tk.CTkCheckBox(ventana, text="Kilometers to pick a bicycle", variable=check_kms_coger)
        check_button4 = tk.CTkCheckBox(ventana, text="Kilometers to drop a bicycle", variable=check_kms_dejar)
        check_button5 = tk.CTkCheckBox(ventana, text="Solved Petitions to pick a bicycle",
                                       variable=check_peticionesResueltas_coger)
        check_button6 = tk.CTkCheckBox(ventana, text="Solved Petitions to drop a bicycle",
                                       variable=check_peticionesResueltas_dejar)
        check_button7 = tk.CTkCheckBox(ventana, text="Not solved Petitions to pick a bicycle",
                                       variable=check_peticionesNoResueltas_coger)
        check_button8 = tk.CTkCheckBox(ventana, text="Not solved Petitions to drop a bicycle",
                                       variable=check_peticionesNoResueltas_dejar)

        check_button9 = tk.CTkCheckBox(ventana, text="Unreal kilometers to pick a bicycle", variable=check_kmsFicticios_coger)
        check_button10 = tk.CTkCheckBox(ventana, text="Unreal kilometers to drop a bicycle", variable=check_kmsFicticios_dejar)

        check_button11 = tk.CTkCheckBox(ventana, text="Solved unreal Petitions to pick a bicycle",
                                        variable=check_peticionesResueltas_ficticias_coger)

        check_button12 = tk.CTkCheckBox(ventana, text="Solved unreal Petitions to drop a bicycle",
                                        variable=check_peticionesResueltas_ficticias_dejar)

        check_button13 = tk.CTkCheckBox(ventana, text="Not solved unreal petitions to pick a bicycle",
                                        variable=check_NoResueltas_ficticias_coger)

        check_button14 = tk.CTkCheckBox(ventana, text="Not solved unreal petitions to drop a bicycle",
                                        variable=check_NoResueltas_ficticias_dejar)

        check_button15 = tk.CTkCheckBox(ventana, text="Custom Matrix",
                                        variable=check_Matriz_Custom)



        # Colocamos el checkbox en la ventana
        fondo_ventana = ventana.cget("bg")
        separator1 = tt.Frame(ventana,height=20,bg=fondo_ventana)
        separator2 = tt.Frame(ventana, height=20, bg=fondo_ventana)
        separator3 = tt.Frame(ventana, height=20, bg=fondo_ventana)

        check_button1.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button2.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        separator1.pack(fill="x")
        check_button3.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button4.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button9.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button10.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        separator2.pack(fill="x")

        check_button5.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button6.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button7.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button8.pack(side=tk.TOP, pady=5, padx=1, anchor="w")

        check_button11.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button12.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button13.pack(side=tk.TOP, pady=5, padx=1, anchor="w")
        check_button14.pack(side=tk.TOP, pady=5, padx=1, anchor="w")

        separator3.pack(fill="x")
        check_button15.pack(side=tk.TOP, pady=5, padx=1, anchor="w")

    # Función perteneciente del bloque encargado de cambiar las deltas times de los datos
    def __cambiarDeltas(self, ventana):

        titulo = tk.CTkLabel(
            master=ventana,
            text="Select the deltas to transform:",
            font=("Arial", 20),
        )
        titulo.place(relx=0.6, rely=0.2)

        texto_deltasActuales = tk.CTkLabel(
            master=ventana,
            text="Size of the current delta:",
            font=("Arial", 10),
        )

        texto_deltasFinales = tk.CTkLabel(
            master=ventana,
            text="Size of the new delta:",
            font=("Arial", 10),
        )
        texto_explicacion = tk.CTkLabel(
            master=ventana,
            text="Support of delta transformation:",
            font=("Arial", 15),
        )

        texto_explicacion_leyenda = tk.CTkLabel(
            master=ventana,
            text="1 Hour          -> 60 deltas \n"
                 "1 Day           -> 1440 deltas \n"
                 "1 Week          -> 10080 deltas \n"
                 "30-day month    -> 43200 deltas \n"
                 "31-day month    -> 44640 deltas",
            font=("Courier", 15),
            justify="left",
            padx=10
        )
        texto_explicacion.place(relx=0.6, rely=0.4)
        texto_explicacion_leyenda.place(relx=0.6, rely=0.45)

        texto_deltasActuales.place(relx=0.5,rely=0.3)
        self.textbox_deltasActuales.place(relx=0.6, rely=0.3)
        self.textbox_deltasActuales.insert(tk.END, "15")

        texto_deltasFinales.place(relx=0.7, rely=0.3)
        self.textbox_deltasTransformar.place(relx=0.8, rely=0.3)
        self.textbox_deltasTransformar.insert(tk.END, "60")
        check_mediaOacumulada = tk.CTkCheckBox(ventana, text="Average/Cumulative", variable=self.delta_media)
        check_mediaOacumulada.place(relx=0.9, rely=0.3)

    # Metodos para mostrar las opciones de los gráficos

    def __mostrarSeleccionEstacionDias(self):

        self.labels_titulos['seleccionEstacionDias'].place(relx=0.6, rely=0.65)

        self.textbox_estacion.place(relx=0.6, rely=0.7)
        self.textbox_dias.place(relx=0.7, rely=0.7)

    def __ocultarSeleccionEstacionDias(self):
        self.labels_titulos['seleccionEstacionDias'].place_forget()
        self.textbox_estacion.place_forget()
        self.textbox_dias.place_forget()

    def __mostrarSeleccionHistogramaDiario(self):

        self.labels_titulos['seleccionHistogramaDiario'].place(relx=0.6, rely=0.65)
        self.textbox_dias.place(relx=0.6, rely=0.7)
        self.check_histogramaMediaAcumulada.place(relx=0.7, rely=0.7)
        self.check_frecuencia.place(relx=0.85, rely=0.7)

    def __ocultarSeleccionHistogramaDiario(self):
        self.labels_titulos['seleccionHistogramaDiario'].place_forget()
        self.textbox_dias.place_forget()
        self.check_histogramaMediaAcumulada.place_forget()
        self.check_frecuencia.place_forget()

    def __mostrarSeleccionGraficaComparacionEstaciones(self):
        self.labels_titulos['seleccionGraficaComparacionEstaciones'].place(relx=0.6, rely=0.65)
        self.textbox_estacion.place(relx=0.6, rely=0.7)
        self.textbox_dias.place(relx=0.7, rely=0.7)

    def __ocultarSeleccionGraficaComparacionEstaciones(self):
        self.labels_titulos['seleccionGraficaComparacionEstaciones'].place_forget()
        self.textbox_estacion.place_forget()
        self.textbox_dias.place_forget()

    def __mostrarSeleccionGraficaComparacionMatrices(self):
        self.labels_titulos['seleccionGraficaComparacionMatrices'].place(relx=0.6, rely=0.65)
        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMA'].place(relx=0.45,rely=0.7)
        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMC'].place(relx=0.65,rely=0.8)
        self.labels_titulos['seleccionGraficaComparacionMatricesDeltaMC'].place(relx=0.35,rely=0.8)
        self.textbox_estacion.place(relx=0.6, rely=0.7)
        self.check_histogramaMediaAcumulada.place(relx=0.8, rely=0.7)
        self.textbox_deltaCustom.place(relx=0.5, rely=0.8)
        self.textbox_estacionesCustom.place(relx=0.85, rely=0.8)

    def __ocultarSeleccionGraficaComparacionMatrices(self):
        self.labels_titulos['seleccionGraficaComparacionMatrices'].place_forget()
        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMA'].place_forget()
        self.labels_titulos['seleccionGraficaComparacionMatricesEstacionesMC'].place_forget()
        self.labels_titulos['seleccionGraficaComparacionMatricesDeltaMC'].place_forget()
        self.textbox_estacion.place_forget()
        self.check_histogramaMediaAcumulada.place_forget()
        self.textbox_deltaCustom.place_forget()
        self.textbox_estacionesCustom.place_forget()

    def __seleccionarEstadisticas(self):

        self.combobox.place(relx=0.3, rely=0.3)
        self.combobox.set("Select the statistic")

    def __getBotonesPulsados(self):
        try:
            seleccionados = []
            for i in range(len(self.listaMatrices)):
                if self.listaMatrices[i].get():
                    seleccionados.append(Constantes.LISTA_MATRICES[i])

            ###Selección de matrices:

            # En la lista seleccionados tenemos todas las matrices seleccionadas para su unificación.
            # En la lista seleccionados tenemos todas las matrices seleccionadas para su unificación.
            inicio = 0
            if not self.checkmatrizCustom.get() or Constantes.MATRIZ_CUSTOM == None:
                matrizDeseada = self.matrices[seleccionados[0]].matrix
                inicio = 1
            else:
                matrizDeseada = Constantes.MATRIZ_CUSTOM.matrix
                inicio = 0

            if len(seleccionados) > 1:
                for i in range(inicio, len(seleccionados)):
                    matrizDeseada = Agrupador.agruparMatrices(matrizDeseada, self.matrices[seleccionados[i]].matrix)

            ###Configuración de deltas:
            # Compruebo que exista texto.
            matrizDeseada = auxiliaresCalculos.rellenarFilasMatrizDeseada(matrizDeseada,
                                                                          self.matrices[Constantes.OCUPACION].matrix.shape[0] - 1)

            if not self.textbox_deltasActuales.get("0.0", 'end-1c') == "" or not self.textbox_deltasActuales.get("0.0",
                                                                                                                 'end-1c') == "":
                aux_deltaInicial = int(self.textbox_deltasActuales.get("0.0", 'end-1c'))
                aux_deltaFinal = int(self.textbox_deltasTransformar.get("0.0", 'end-1c'))
                if self.delta_media.get():  # Si el usuario quiere agrupar por media:
                    matrizDeseada = Agrupador.colapsarDeltasMedia(matrizDeseada, aux_deltaInicial, aux_deltaFinal)
                else:
                    matrizDeseada = Agrupador.colapsarDeltasAcumulacion(matrizDeseada, aux_deltaInicial, aux_deltaFinal)
                Constantes.DELTA_TIME = aux_deltaFinal

            eOH = estadisticasOcupacionHorarias(matrizDeseada, Constantes.DELTA_TIME)
            diasMatrizDeseada = int(matrizDeseada.shape[0] / 24)
            if self.combobox.get() == "Accumulated graph of a station":
                dias_escogidos = 0
                estacion_elegida = 0
                if not self.textbox_dias.get("0.0", 'end-1c') == "":

                    if self.textbox_dias.get("0.0", 'end-1c') == 'all':
                        dias_escogidos = list(range(diasMatrizDeseada))
                    else:
                        dias_escogidos = list(map(int, self.textbox_dias.get("0.0", 'end-1c').split(',')))

                if not self.textbox_estacion.get("0.0", 'end-1c') == "":
                    estacion_elegida = int(self.textbox_estacion.get("0.0", 'end-1c'))
                eOH.HistogramaAcumulacion(estacion_elegida, dias_escogidos)
            else:
                if self.combobox.get() == "Average graph of a station":
                    dias_escogidos = 0
                    estacion_elegida = 0
                    if not self.textbox_dias.get("0.0", 'end-1c') == "":
                        if self.textbox_dias.get("0.0", 'end-1c') == 'all':
                            dias_escogidos = list(range(diasMatrizDeseada))
                        else:
                            dias_escogidos = list(map(int, self.textbox_dias.get("0.0", 'end-1c').split(',')))

                    if not self.textbox_estacion.get("0.0", 'end-1c') == "":
                        estacion_elegida = int(self.textbox_estacion.get("0.0", 'end-1c'))
                    eOH.HistogramaPorEstacion(estacion_elegida, dias_escogidos)
                else:
                    if self.combobox.get() == "Bar graph Average of all stations":
                        dias_escogidos = 0

                        if not self.textbox_dias.get("0.0", 'end-1c') == "":
                            if self.textbox_dias.get("0.0", 'end-1c') == 'all':
                                dias_escogidos = list(range(diasMatrizDeseada))
                            else:
                                dias_escogidos = list(map(int, self.textbox_dias.get("0.0", 'end-1c').split(',')))

                        self.check_histogramaMediaAcumulada.get()

                        eOH.HistogramaOcupacionMedia(dias_escogidos, frecuencia=self.check_frecuencia.get(),
                                                     media=self.check_histogramaMediaAcumulada.get())
                    else:
                        if self.combobox.get() == "Graph comparing stations":

                            estaciones_elegidas = 0

                            if not self.textbox_estacion.get("0.0", 'end-1c') == "":
                                estaciones_elegidas = list(map(int, self.textbox_estacion.get("0.0", 'end-1c').split(',')))

                            diasComparacion = []
                            for i in range(len(estaciones_elegidas)):
                                dias_aux = self.textbox_dias.get("0.0", 'end-1c').split("#")[i]
                                if dias_aux == "all":
                                    lista_dias = list(range(0, diasMatrizDeseada))
                                else:
                                    lista_dias = list(map(int, dias_aux.split(",")))
                                diasComparacion.append(lista_dias)

                            eOH.HistogramaCompararEstaciones(estaciones_elegidas, diasComparacion,media=self.delta_media.get())
                        else:
                            if self.combobox.get() == "Graph comparing matrices":
                                estaciones_elegidas_m1 = 0

                                if not self.textbox_estacion.get("0.0", 'end-1c') == "":
                                    estaciones_elegidas_m1 = list(
                                        map(int, self.textbox_estacion.get("0.0", 'end-1c').split(',')))

                                estaciones_elegidas_m2 = 0
                                if not self.textbox_estacionesCustom.get("0.0", 'end-1c') == "":
                                    estaciones_elegidas_m2 = list(
                                        map(int, self.textbox_estacionesCustom.get("0.0", 'end-1c').split(',')))

                                deltaCustom = int(self.textbox_deltaCustom.get("0.0", 'end-1c'))
                                eOH.HistogramaCompararMatrices(Constantes.MATRIZ_CUSTOM, deltaCustom,
                                                               estaciones_elegidas_m1, estaciones_elegidas_m2,
                                                               media=self.check_histogramaMediaAcumulada.get())
        except:
            self.mostrar_advertencia()

    def mostrar_advertencia(self):
        messagebox.showwarning("Warning", "There are still parameters to be filled in")

    def seleccionarGrafico(self, opcion_seleccionada):

        if opcion_seleccionada == "Accumulated graph of a station" or opcion_seleccionada == "Average graph of a station":
            self.__ocultarSeleccionHistogramaDiario()
            self.__ocultarSeleccionGraficaComparacionEstaciones()
            self.__ocultarSeleccionGraficaComparacionMatrices()
            self.__mostrarSeleccionEstacionDias()
        else:
            if opcion_seleccionada == "Bar graph Average of all stations":
                self.__ocultarSeleccionEstacionDias()
                self.__ocultarSeleccionGraficaComparacionEstaciones()
                self.__ocultarSeleccionGraficaComparacionMatrices()
                self.__mostrarSeleccionHistogramaDiario()
            else:

                if opcion_seleccionada == "Graph comparing stations":
                    self.__ocultarSeleccionHistogramaDiario()
                    self.__ocultarSeleccionEstacionDias()
                    self.__ocultarSeleccionGraficaComparacionMatrices()
                    self.__mostrarSeleccionGraficaComparacionEstaciones()

                else:
                    if opcion_seleccionada == "Graph comparing matrices":
                        self.__ocultarSeleccionHistogramaDiario()
                        self.__ocultarSeleccionEstacionDias()
                        self.__ocultarSeleccionGraficaComparacionEstaciones()
                        self.__mostrarSeleccionGraficaComparacionMatrices()
