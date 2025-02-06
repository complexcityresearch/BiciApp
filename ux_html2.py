import os

import wx
import wx.html2 as html2

from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion


class MyFrame(wx.Frame):

    def __init__(self, parent,interfaz_representacion: Interfaz_Representacion,instanteInicial=0):
        super().__init__(parent, title="Web Viewer", size=(800, 600))
        self.instanteActual = instanteInicial
        self.text_instante = wx.TextCtrl(self)
        self.representacion = interfaz_representacion
        # Crear el control WebView
        self.webview = html2.WebView.New(self)

        # Cargar el archivo HTML

        #current_dir = os.getcwd()
        html_file = os.path.join(os.getcwd(), "MapaEspera.html")
        #html_file = interfaz_representacion.getFichero()
        # Crear el control WebView
        self.webview = html2.WebView.New(self)

        # Cargar el archivo HTML
        url = "file:///" + html_file.replace("\\", "/")
        self.webview.LoadURL(url)

        # Agregar el control WebView al sizer principal

        self.__agregarBotones()
        # Mostrar la ventana
        #wx.CallAfter(self.cargarInstante, "Prueba")
        self.Show()
        #self.cargarInstante(None)

    def cargarHTML(self):
        html_file = self.representacion.getFichero()
        # Cargar el archivo HTML
        url = "file:///" + html_file.replace("\\", "/")
        self.webview.LoadURL(url)
        #self.Show()

    def __agregarBotones(self):
        # Crear un sizer principal para organizar los widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.webview, 1, wx.EXPAND)


        # Crear un sizer horizontal para los botones y el cuadro de texto
        button_text_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Crear los botones
        button1 = wx.Button(self, label="<")
        button2 = wx.Button(self, label=">")
        self.button3 = wx.Button(self,label="Load instant")

        button1.Bind(wx.EVT_BUTTON, self.botonPulsadoDecrementar)
        button2.Bind(wx.EVT_BUTTON, self.botonPulsadoIncrementar)
        self.button3.Bind(wx.EVT_BUTTON, self.cargarInstante)

        # Crear el cuadro de texto

        self.text_instante.WriteText(str(self.instanteActual))

        # Agregar los botones y el cuadro de texto al sizer horizontal
        button_text_sizer.Add(self.button3, 0, wx.ALL, 5)
        button_text_sizer.Add(button1, 0, wx.ALL, 5)
        button_text_sizer.Add(button2, 0, wx.ALL, 5)
        button_text_sizer.Add(self.text_instante, 1, wx.EXPAND | wx.ALL, 5)

        # Agregar el sizer horizontal al sizer principal
        sizer.Add(button_text_sizer, 0, wx.EXPAND)

        # Establecer el sizer principal en la ventana
        self.SetSizer(sizer)

    def botonPulsadoIncrementar(self,event):
        #self.instanteActual = int(self.text_instante.GetValue())
        nuevoInst = str(int(self.instanteActual) + 1)
        self.text_instante.ChangeValue(nuevoInst)
        self.cargarInstante(None)

    def botonPulsadoDecrementar(self,event):
        #self.instanteActual = int(self.text_instante.GetValue())
        nuevoInst = str(int(self.instanteActual) - 1)
        self.text_instante.ChangeValue(nuevoInst)
        self.cargarInstante(None)

    def cargarInstante(self,event):
        self.instanteActual = int(self.text_instante.GetValue())
        self.representacion.cargarMapaInstante(self.instanteActual)
        self.cargarHTML()


'''
app = wx.App()
frame = MyFrame(None)
app.MainLoop()'''