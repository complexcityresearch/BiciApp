
import wx

from Backend import Constantes
from Backend.Auxiliares import auxiliaresCalculos
from Backend.Manipuladores import Agrupador
from Backend.Representacion.ManejadorMapas.manejar_Voronoi import manejar_Voronoi
from Backend.Representacion.ManejadorMapas.manejar_densidad import Manejar_Densidad
from Backend.Representacion.ManejadorMapas.manejar_mapaCirculos import manejar_mapaCirculos

from Frontend.Ventana import Ventana
import customtkinter as tk
from ux_html2 import MyFrame

import tkinter as tt
from tkinter import ttk, messagebox


class VentanaMapa2(Ventana):

    def __init__(self,matrices:dict):
        super().__init__("Map Generator")
        ventana = super().getVentanaAttribute()
        #Variables:
        self.matrices = matrices
        self.delta_media = tk.BooleanVar()
        self.textbox_deltasActuales = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_deltasTransformar = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_listaEstaciones = tk.CTkTextbox(master=ventana, height=5, width=180)
        self.checkmatrizCustom = None
        self.combobox = tk.CTkOptionMenu(master=ventana,
                                         values=["Density Map",
                                                 "Voronoi Map",
                                                 "Circles Map"]
                                         )
        self.opcionesPaleta = ["Green Scale", "Magma","Circle of colors"]

        self.combobox.place(relx=0.3, rely=0.3)
        self.combobox.set("Select a statistic")
        #Ventana:
        self.__titulo(ventana)
        self.__seleccionMatrices(ventana)
        self.__boton(ventana)
        self.__cambiarDeltas(ventana)
        self.__seleccionarEstaciones(ventana)
        texto_paletas = tk.CTkLabel(
            master=ventana,
            text="Palette selection for positive and negative values:",
            font=("Arial", 15),
        )
        texto_paletas.place(relx=0.3, rely=0.4)
        self.combobox_positivos = tk.CTkOptionMenu(master=ventana,
                                                   values=self.opcionesPaleta,

                                                   )
        self.combobox_positivos.set(self.opcionesPaleta[1])
        self.combobox_positivos.place(relx=0.3, rely=0.5)
        self.combobox_negativos = tk.CTkOptionMenu(master=ventana,
                                                   values=self.opcionesPaleta,

                                                   )
        self.combobox_negativos.set(self.opcionesPaleta[0])
        self.combobox_negativos.place(relx=0.3, rely=0.6)
        super().ejecutarVentana()


    def __titulo(self,ventana):
        titulo = tk.CTkLabel(
            master = ventana,
            text = "Map Generator",
            font=("Arial",70),
        )
        descripcion = tk.CTkLabel(
            master=ventana,
            text="Matrices to be represented",
            font=("Arial", 20),
        )
        #titulo.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        titulo.pack()
        descripcion.pack(side = tk.TOP,pady=5,padx=1,anchor="w")

    def __boton(self,ventana):
        boton = tk.CTkButton(master=ventana, text="Generate Map",
                                   command=lambda: self.__getBotonesPulsados())
        boton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def __seleccionMatrices(self,ventana):
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
        separator1 = tt.Frame(ventana, height=20, bg=fondo_ventana)
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

        texto_deltasActuales.place(relx=0.5, rely=0.3)
        self.textbox_deltasActuales.place(relx=0.6, rely=0.3)
        self.textbox_deltasActuales.insert(tk.END, "15")

        texto_deltasFinales.place(relx=0.7, rely=0.3)
        self.textbox_deltasTransformar.place(relx=0.8, rely=0.3)
        self.textbox_deltasTransformar.insert(tk.END, "60")
        check_mediaOacumulada = tk.CTkCheckBox(ventana, text="Average/Cumulative", variable=self.delta_media)
        check_mediaOacumulada.place(relx=0.9, rely=0.3)

    #Funcion para el interfaz de seleccionar estaciones:
    def __seleccionarEstaciones(self,ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Select the stations to be represented:",
            font=("Arial", 20),
        )
        titulo.place(relx=0.6, rely=0.6)

        self.textbox_listaEstaciones.place(relx=0.6, rely=0.7)

    def __getBotonesPulsados(self):
        try:
            seleccionados = []
            for i in range(len(self.listaMatrices)):
                if self.listaMatrices[i].get():
                    seleccionados.append(Constantes.LISTA_MATRICES[i])

            ###Selección de matrices:

            #En la lista seleccionados tenemos todas las matrices seleccionadas para su unificación.
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
            matrizDeseada = auxiliaresCalculos.rellenarFilasMatrizDeseada(matrizDeseada,
                                                                          self.matrices[Constantes.OCUPACION].matrix.shape[
                                                                              0] - 1)
            ###Configuración de deltas:
            #Compruebo que exista texto.

            if not self.textbox_deltasActuales.get("0.0", 'end-1c') == "" or not self.textbox_deltasActuales.get("0.0", 'end-1c') == "":
                aux_deltaInicial = int(self.textbox_deltasActuales.get("0.0", 'end-1c'))
                aux_deltaFinal = int(self.textbox_deltasTransformar.get("0.0", 'end-1c'))
                if self.delta_media.get():#Si el usuario quiere agrupar por media:
                    matrizDeseada=Agrupador.colapsarDeltasMedia(matrizDeseada,aux_deltaInicial,aux_deltaFinal)
                else:
                    matrizDeseada = Agrupador.colapsarDeltasAcumulacion(matrizDeseada, aux_deltaInicial, aux_deltaFinal)
                Constantes.DELTA_TIME = aux_deltaFinal

            try:

                #Comprobar la lista de estaciones a representar.
                listaEstaciones = None
                if not self.textbox_listaEstaciones.get("0.0", 'end-1c') == "":
                    cadenaSinParsear = self.textbox_listaEstaciones.get("0.0", 'end-1c')
                    listaEstaciones = list(map(int, cadenaSinParsear.split(",")))

                if self.combobox.get() == "Density Map":
                    man_vor = Manejar_Densidad(matrizDeseada, Constantes.COORDENADAS,listaEstaciones=listaEstaciones)
                    app = wx.App()
                    frame = MyFrame(None, man_vor)
                    app.MainLoop()
                else:
                    if self.combobox.get() == "Voronoi Map":

                        man_vor = manejar_Voronoi(matrizDeseada, Constantes.COORDENADAS,escalaPositivos=self.combobox_positivos.get(),escalaNegativos=self.combobox_negativos.get())
                        app = wx.App()
                        frame = MyFrame(None, man_vor)
                        app.MainLoop()

                    else:
                        if self.combobox.get() == "Circles Map":
                            '''
                            man_cir = manejar_mapaCirculos(matrizDeseada, Constantes.COORDENADAS)
                            obj = InterfazHTML(man_cir)
                            obj.interfazWeb()'''
                            man_cir = manejar_mapaCirculos(matrizDeseada, Constantes.COORDENADAS, listaEstaciones=listaEstaciones)
                            app = wx.App()
                            frame = MyFrame(None,man_cir)
                            app.MainLoop()



            except Exception as e:
                print("Unknown error:", e)
        except:
            self.mostrar_advertencia()

    def mostrar_advertencia(self):
        messagebox.showwarning("Warning", "There are still parameters to be filled in")