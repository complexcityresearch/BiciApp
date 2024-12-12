from tkinter import messagebox

import wx

from Backend import Constantes
from Backend.Manipuladores import Agrupador
from Backend.Representacion.ManejadorMapas.Manejar_Desplazamientos import Manejar_Desplazamientos
from Frontend.Ventana import Ventana
import customtkinter as tk

from ux_html2 import MyFrame


class VentanaDesplazamientos(Ventana):


    def __init__(self,matrizDesplazamientos):
        super().__init__("Displacement maps")
        self.matrizDesplazamientos = matrizDesplazamientos
        ventana = super().getVentanaAttribute()
        self.__titulo(ventana)
        self.instanteRepresentar = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_deltasActuales = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.textbox_deltasTransformar = tk.CTkTextbox(master=ventana, height=5, width=135)
        self.check_tipo_movimiento = tk.BooleanVar()
        self.check_tipo_peticion = tk.BooleanVar()
        self.labelTextos = {}
        self.__cargarTextos(ventana)
        self.__cambiarDeltas(ventana)
        self.__colocarElementos(ventana)
        self.__boton(ventana)
        super().ejecutarVentana()


    def __titulo(self, ventana):
        titulo = tk.CTkLabel(
            master=ventana,
            text="Displacement maps",
            font=("Arial", 70),
        )
        titulo.pack()

    def __cargarTextos(self,ventana):
        self.labelTextos['instante'] = tk.CTkLabel(
            master=ventana,
            text="Enter the instant to be represented: ",
            font=("Arial", 20),
        )
        self.labelTextos['Tipo de accion'] = tk.CTkLabel(
            master=ventana,
            text="Check for walking routes, uncheck for cycling routes: ",
            font=("Arial", 10),
        )
        self.labelTextos['Tipo de peticion'] = tk.CTkLabel(
            master=ventana,
            text="Check for real requests, uncheck for fictitious: ",
            font=("Arial", 10),
        )

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
                 "1 Week        -> 10080 deltas \n"
                 "30-day month   -> 43200 deltas \n"
                 "31-day month   -> 44640 deltas",
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



    def __colocarElementos(self,ventana):
        self.labelTextos['instante'].place(relx=0.1,rely=0.2)
        self.instanteRepresentar.place(relx = 0.1, rely=0.3)
        self.labelTextos['Tipo de accion'].place(relx=0.1,rely=0.4)
        check_button2 = tk.CTkCheckBox(ventana, text="Andar/Bicicleta", variable=self.check_tipo_movimiento)
        check_button2.place(relx=0.1,rely=0.5)
        self.labelTextos['Tipo de peticion'].place(relx=0.1,rely=0.6)
        check_button3 = tk.CTkCheckBox(ventana, text="Reales/Ficticios", variable=self.check_tipo_peticion)
        check_button3.place(relx=0.1, rely=0.7)


    def __boton(self, ventana):
        boton = tk.CTkButton(master=ventana, text="Generate Map",
                             command=self.__generarMapaDesplazamiento)
        boton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def __generarMapaDesplazamiento(self):
        try:
            matrizDeseada = self.matrizDesplazamientos
            if not self.textbox_deltasActuales.get("0.0", 'end-1c') == "" or not self.textbox_deltasActuales.get("0.0",
                                                                                                                 'end-1c') == "":
                aux_deltaInicial = int(self.textbox_deltasActuales.get("0.0", 'end-1c'))
                aux_deltaFinal = int(self.textbox_deltasTransformar.get("0.0", 'end-1c'))
                matrizDeseada = Agrupador.colapsarDesplazamientos(matrizDeseada,aux_deltaInicial,aux_deltaFinal)

            instante =0
            if not self.instanteRepresentar.get("0.0", 'end-1c') == "":
                instante = int(self.instanteRepresentar.get("0.0", 'end-1c'))

            tipo = 0
            if self.check_tipo_movimiento.get():
                tipo = 1
            else:
                tipo = -1

            md = Manejar_Desplazamientos(matrizDeseada,Constantes.COORDENADAS,accion=tipo,tipo=self.check_tipo_peticion.get())
            #md.cargarMapaInstante(instante)
            app = wx.App()
            frame = MyFrame(None, md,instante)
            app.MainLoop()
        except:
            self.mostrar_advertencia()
    def mostrar_advertencia(self):
        messagebox.showwarning("Warning", "There are still parameters to be filled in")

