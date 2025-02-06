import math
import operator


from Backend import Constantes
from Backend.Auxiliares import auxiliaresCalculos
from Backend.Manipuladores import Agrupador
from Backend.Manipuladores.Filtrador import Filtrador

from Frontend.Ventana import Ventana
import customtkinter as tk
from tkinter import messagebox,Toplevel,Text,Button
import tkinter as tt

# Clase que contiene la interfaz del filtrado de datos.
# Realiza consultas a los datos
class VentanaFiltrador2(Ventana):

    def __init__(self, matrices: dict):
        super().__init__("Filter")
        self.matrices = matrices
        self.listaMatrices = []
        ventana = super().getVentanaAttribute()
        self.delta_media = tk.BooleanVar()
        self.textbox_deltasActuales = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_deltasTransformar = tk.CTkTextbox(master=ventana, height=5, width=135)

        # Parametros del filtrado:
        self.checkmatrizCustom = None
        self.textbox_arg1 = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_arg2 = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_arg3 = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_arg4 = tk.CTkTextbox(master=ventana, height=5, width=135)

        self.texto1 = tk.CTkLabel(master=ventana)
        self.texto2 = tk.CTkLabel(master=ventana)
        self.texto3 = tk.CTkLabel(master=ventana)
        self.texto4 = tk.CTkLabel(master=ventana)
        self.labels_titulos = {}
        self.__cargarLabels(ventana)
        self.combobox = tk.CTkOptionMenu(master=ventana,
                                         values=["Query stations above a value",
                                                 "Consult stations higher than one value for the whole month",
                                                 "Query the hours where there is a percentage of stations above a certain value",
                                                 "Query the percentage of the time where the stations are above a certain value"],

                                         command=self.optionmenu_callback,
                                         )

        self.__titulo(ventana)
        self.__seleccionMatrices(ventana)
        self.__boton(ventana)
        self.__seleccionarFiltro(ventana)
        self.__cambiarDeltas(ventana)
        super().ejecutarVentana()

    def optionmenu_callback(self,choice):

        self.__cargarParametrosFiltrado()


    def __titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Filter",
            font=("Arial", 70),
        )
        descripcion = tk.CTkLabel(
            master=ventana,
            text="Matrices to Filter",
            font=("Arial", 20),
        )
        # titulo.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        titulo.pack()
        descripcion.pack(side=tk.TOP, pady=5, padx=1, anchor="w")

    def __boton(self, ventana):
        boton = tk.CTkButton(master=ventana, text="Perform Filtering",
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
            text="Current delta size:",
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

        texto_deltasFinales.place(relx=0.7, rely=0.3)
        self.textbox_deltasTransformar.place(relx=0.8, rely=0.3)
        check_mediaOacumulada = tk.CTkCheckBox(ventana, text="Average", variable=self.delta_media)
        check_mediaOacumulada.place(relx=0.9, rely=0.3)



    def __seleccionarFiltro(self, ventana):

        self.combobox.place(relx=0.2, rely=0.2)
        self.combobox.set("Select filter")

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
                                                                          self.matrices[Constantes.OCUPACION].matrix.shape[
                                                                              0] - 1)
            if not self.textbox_deltasActuales.get("0.0", 'end-1c') == "" or not self.textbox_deltasActuales.get("0.0",
                                                                                                                 'end-1c') == "":
                aux_deltaInicial = int(self.textbox_deltasActuales.get("0.0", 'end-1c'))
                aux_deltaFinal = int(self.textbox_deltasTransformar.get("0.0", 'end-1c'))
                if self.delta_media.get():  # Si el usuario quiere agrupar por media:
                    matrizDeseada = Agrupador.colapsarDeltasMedia(matrizDeseada, aux_deltaInicial, aux_deltaFinal)
                else:
                    matrizDeseada = Agrupador.colapsarDeltasAcumulacion(matrizDeseada, aux_deltaInicial, aux_deltaFinal)
                Constantes.DELTA_TIME = aux_deltaFinal

            filtrador = Filtrador(matrizDeseada, Constantes.DELTA_TIME)

            if self.combobox.get() == "Query stations above a value":
                operadorYvalor = self.textbox_arg1.get("0.0", 'end-1c')
                veces = self.textbox_arg2.get("0.0", 'end-1c')
                dia = self.textbox_arg3.get("0.0", 'end-1c')

                operador, valor, nombreOperador = self.__obtenerOperador(operadorYvalor)
                resultado = filtrador.consultarEstacionesSuperioresAUnValor(int(valor), int(veces),
                                                                            int(dia), operador=operador)
                self.__mostrarResultado(str(resultado))

            else:
                if self.combobox.get() == "Consult stations higher than one value for the whole month":
                    operadorYvalor = self.textbox_arg1.get("0.0", 'end-1c')
                    veces = self.textbox_arg2.get("0.0", 'end-1c')

                    if 'all' in self.textbox_arg3.get("0.0", 'end-1c'):
                        diasEnMatriz = math.trunc(matrizDeseada.shape[0] / ((60 / Constantes.DELTA_TIME) * 24))
                        lista_dias = list(range(0, diasEnMatriz))
                    else:

                        lista_dias = self.textbox_arg3.get("0.0", 'end-1c')
                        lista_dias = list(map(int, lista_dias.split(",")))

                    dias_perdon = int(self.textbox_arg4.get("0.0", 'end-1c'))

                    operador, valor, nombreOperador = self.__obtenerOperador(operadorYvalor)
                    resultado = filtrador.consultarEstacionesSuperioresAUnValorEnVariosDias(int(valor), int(veces),
                                                                                lista_dias,dias_perdon, operador=operador)
                    self.__mostrarResultado(str(resultado))
                else:
                    if self.combobox.get() == "Query the hours where there is a percentage of stations above a certain value":
                        operadorYvalor = self.textbox_arg1.get("0.0", 'end-1c')
                        porcentajeEstaciones = self.textbox_arg2.get("0.0", 'end-1c')

                        operador, valor, nombreOperador = self.__obtenerOperador(operadorYvalor)
                        resultado = filtrador.consultarHorasEstacionesSuperioresAUnValor(int(valor), float(porcentajeEstaciones),
                                                                                    operador=operador)
                        self.__mostrarResultado(str(resultado))

                    else:
                        if self.combobox.get() == "Query the percentage of the time where the stations are above a certain value":
                            operadorYvalor = self.textbox_arg1.get("0.0", 'end-1c')

                            if 'all' in self.textbox_arg2.get("0.0", 'end-1c'):
                                listaEstaciones = list(range(matrizDeseada.shape[1]-1))
                            else:
                                listaEstaciones = self.textbox_arg2.get("0.0", 'end-1c')
                                listaEstaciones = list(map(int, listaEstaciones.split(",")))

                            operador, valor, nombreOperador = self.__obtenerOperador(operadorYvalor)
                            resultado = filtrador.consultarPorcentajeTiempoEstacionSuperiorAUnValor(int(valor),
                                                                                             listaEstaciones,
                                                                                             operador=operador)
                            self.__mostrarResultado(str(resultado))
        except:
            self.mostrar_advertencia()

    def mostrar_advertencia(self):
        messagebox.showwarning("Warning", "There are still parameters to be filled in")
    def __cargarLabels(self, ventana):
        sizeText = 15
        self.labels_titulos['OperadorYValor'] = tk.CTkLabel(
            master=ventana,
            text="Enter operator and value :",
            font=("Arial", sizeText),

        )
        self.labels_titulos['Veces'] = tk.CTkLabel(
            master=ventana,
            text="Enter the minimum number of times in a day :",
            font=("Arial", sizeText),

        )

        self.labels_titulos['Dias'] = tk.CTkLabel(
            master=ventana,
            text="Enter the day/days:",
            font=("Arial", sizeText),

        )
        self.labels_titulos['DiasPerdon'] = tk.CTkLabel(
            master=ventana,
            text="Enter the exception days :",
            font=("Arial", sizeText),

        )
        self.labels_titulos['PorcentajeEstaciones'] = tk.CTkLabel(
            master=ventana,
            text="Enter the percentage of stations out of 100 :",
            font=("Arial", 10),

        )
        self.labels_titulos['ListaEstaciones'] = tk.CTkLabel(
            master=ventana,
            text="Enter the list of station ids :",
            font=("Arial", sizeText),

        )
    def __limpiarInterfaz(self):
        self.textbox_arg1.place_forget()
        self.textbox_arg2.place_forget()
        self.textbox_arg3.place_forget()
        self.textbox_arg4.place_forget()
        for i in self.labels_titulos.keys():
            self.labels_titulos[i].place_forget()


    def __cargarParametrosFiltrado(self):
        self.__limpiarInterfaz()

        if self.combobox.get() == "Query stations above a value" or self.combobox.get() == "Consult stations higher than one value for the whole month":

            self.labels_titulos['OperadorYValor'].place(relx=0.6,rely=0.6)
            self.textbox_arg1.place(relx=0.8, rely=0.6)
            self.labels_titulos['Veces'].place(relx=0.6,rely=0.7)
            self.textbox_arg2.place(relx=0.8, rely=0.7)
            self.labels_titulos['Dias'].place(relx=0.6,rely=0.8)
            self.textbox_arg3.place(relx=0.8, rely=0.8)

            if self.combobox.get() == "Consult stations higher than one value for the whole month":
                self.labels_titulos['DiasPerdon'].place(relx=0.6, rely=0.95)
                self.textbox_arg4.place(relx=0.8, rely=0.95)

        else:

            if self.combobox.get() == "Query the hours where there is a percentage of stations above a certain value":
                self.labels_titulos['OperadorYValor'].place(relx=0.6, rely=0.6)
                self.textbox_arg1.place(relx=0.8, rely=0.6)
                self.labels_titulos['PorcentajeEstaciones'].place(relx=0.6, rely=0.7)
                self.textbox_arg2.place(relx=0.8, rely=0.7)

            else:
                if self.combobox.get() == "Query the percentage of the time where the stations are above a certain value":
                    self.labels_titulos['OperadorYValor'].place(relx=0.6, rely=0.6)
                    self.textbox_arg1.place(relx=0.8, rely=0.6)
                    self.labels_titulos['ListaEstaciones'].place(relx=0.6, rely=0.7)
                    self.textbox_arg2.place(relx=0.8, rely=0.7)


    #Dado un texto, detecta que operador contiene.
    def __obtenerOperador(self,string:str):

        if ">=" in string:
            return operator.ge,string.replace(">=",""),"MAYIGUAL"

        if "<=" in string:
            return operator.le,string.replace("<=",""),"MENIGUAL"

        if ">" in string:
            return operator.gt,string.replace(">",""),"MAY"

        if "<" in string:
            return operator.lt,string.replace("<",""),"MAY"

        #Operador por defecto en caso de que no se identifique la cadena o no se introduzca.
        return operator.ge,string.replace(">=",""),"MAYIGUAL"

    def __mostrarResultado(self,text):
        # Crear la ventana
        window = Toplevel()
        window.geometry("300x200")
        window.title("Resultado: ")

        if '[' in text and ']' in text:
            text = text.replace('[', '').replace(']', '')

        # Crear el objeto Text y establecer el mensaje
        text_box = Text(window)
        text_box.insert("1.0", text)

        # Posicionar el objeto Text y el botón "Copiar" en la ventana
        text_box.pack(fill="both", expand=True)

        # Mostrar la ventana
        window.mainloop()
