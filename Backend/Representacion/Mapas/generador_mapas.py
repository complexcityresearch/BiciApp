import io
import os

from os.path import join

import imageio
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
#import plotly.io as pio
#from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros


#Clase para la representacion con folium
class MapaDensidad:

    def __init__(self,coordenadas:np.ndarray):
        self.datos = pd.DataFrame()
        self.coordenadas = pd.DataFrame(coordenadas,columns=["Estacion","Lat","Long"])
        self.coordenadaCentro = (coordenadas[172,1],coordenadas[172,2])
        '''
        if Constantes.RUTA_SALIDA == "":
            self.app = QtWidgets.QApplication(sys.argv)
            self.textBox = QtWidgets.QSpinBox()

            self.textBox.setMaximum(2**31-1)
            self.mainWindow = None
        '''
        self.instanteActual = 0

    ''' 
    def interfazWeb(self, fig,instancias_max=None):
        html = pio.to_html(fig, full_html=False)
        fig.write_html('density_mapbox.html', auto_open=False)
        #app = QtWidgets.QApplication(sys.argv)
        #self.mainApp=app

        view = QtWebEngineWidgets.QWebEngineView()
        view.load(QtCore.QUrl().fromLocalFile(
            os.getcwd() + "\\density_mapbox.html"
        ))
        view.resize(800, 800)

        view.show()

        main_window = QtWidgets.QMainWindow()
        main_window.resize(800,800)
        main_window.setCentralWidget(view)
        main_window.show()

        control_frame = QtWidgets.QFrame()
        control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        control_layout = QtWidgets.QHBoxLayout()
        control_frame.setLayout(control_layout)

        #----------------------#

        if instancias_max != None:
            label = QtWidgets.QLabel("/"+instancias_max)
        else:
            label = QtWidgets.QLabel("/")

        self.textBox.setValue(self.instanteActual)
        button = QtWidgets.QPushButton("Recargar Mapa")
        boton_navegacion_atras = QtWidgets.QPushButton("<")
        boton_navegacion_delante = QtWidgets.QPushButton(">")

        boton_navegacion_atras.clicked.connect(lambda: self.navegacion(-1))
        button.clicked.connect(lambda: self.botonPulsado())
        boton_navegacion_delante.clicked.connect(lambda: self.navegacion(1))

        # Agregar los widgets al frame

        control_layout.addWidget(self.textBox)
        control_layout.addWidget(label)
        control_layout.addWidget(button)
        control_layout.addWidget(boton_navegacion_atras)
        control_layout.addWidget(boton_navegacion_delante)

        # Agregar el frame al dock widget
        dock = QtWidgets.QDockWidget("Controles", main_window)
        dock.setWidget(control_frame)
        main_window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)

        self.mainWindow = view
        self.app.exec_()


    def botonPulsado(self):
        self.instanteActual = int(self.textBox.text())
        mapa = self.__getMapFigure(int(self.textBox.text()),Constantes.ZOOM_MAPAS_PLOT)
        mapa.write_html('density_mapbox2.html', auto_open=False)

        self.mainWindow.load(QtCore.QUrl().fromLocalFile(
            os.getcwd() + "\\density_mapbox2.html"
        ))

    def navegacion(self,opcion):

        if opcion == -1:
            self.instanteActual -= 1
        else:
            if opcion == 1:
                self.instanteActual +=1
        self.textBox.setValue(self.instanteActual)
        self.botonPulsado()#AutoRefresh.'''


    def cargarDatos(self, datos:pd.DataFrame, lista_estaciones=[]):
        if lista_estaciones == []:
            self.datos= datos
        else:#En el caso de que el usuario desee, ser capaz de representar SOLO las estaciones deseadas.
            datosSinHoras = datos.iloc[:,1:]
            datosFiltrados = datosSinHoras.iloc[:,lista_estaciones]
            datosFiltrados.insert(0, 'UTemp',datos.iloc[:,0] )
            self.datos = datosFiltrados
            self.coordenadas = self.coordenadas.iloc[lista_estaciones,:]
            self.coordenadaCentro = (self.coordenadas.iloc[0,1],self.coordenadas.iloc[0,2])


    # Función de pruba para mostrar un histograma con leyenda.
    def __getMapFigure(self,instante,zoom):
        datos = self.coordenadas.copy()

        valoresAinsertar = self.datos[(self.datos.iloc[:,0] == instante)].iloc[:,1:]
        valorMax = self.datos.iloc[:,1:].max().max()
        opacidad = -1
        if not valoresAinsertar.empty:
            valoresAinsertar = valoresAinsertar.values.tolist()[0]
            datos.insert(3, "Datos",valoresAinsertar)
            valorMin = 0
            opacidad = 1.0
            #datos = datos.append(pd.Series([99999, 0, 0, -20], index=datos.columns), ignore_index=True)
        else:
            datos.insert(3,"Datos",0)
            valorMin =0
            opacidad = 0.0

        # Representar en el mapa.
        #Las librerías de representacion de localizaciones me vuelven loco. Esta librería NO REPRESENTA los valores minimos de los datos
        #¿Porqué? Pues no lo se pero acabo de perder 3 horas el 17/04/2023 para averiguarlo.
        #El valor afecta por supuesto a la escala del color, por lo que es otra cosa a tener en cuenta.



        fig = px.density_mapbox(datos, lat="Lat", lon="Long", z="Datos", radius=50,
                                center=dict(lat=self.coordenadaCentro[0], lon=self.coordenadaCentro[1]),
                                zoom=zoom,
                                mapbox_style="stamen-terrain",
                                hover_data={'Estacion': True},
                                opacity=opacidad,
                                range_color=(valorMin,valorMax))

        fig.update_layout(mapbox=dict(center=dict(lat=self.coordenadaCentro[0], lon=self.coordenadaCentro[1]), zoom=zoom),
                          width=1200, height=1200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def representarHeatmap(self, instante=None , instancias_max = None):
        if instante == None:
            instante = self.instanteActual
        else:
            self.instanteActual = instante
        fig = self.__getMapFigure(instante,Constantes.ZOOM_MAPAS_PLOT)


        if Constantes.RUTA_SALIDA == "":
            #self.interfazWeb(fig,instancias_max)
            #fig.show()
            nombre = "./MapaDensidad.html"
            fig.write_html(nombre, auto_open=False)
        else:
            nombreHTML = auxiliar_ficheros.formatoArchivo("MapaDensidad_instante"+str(self.instanteActual),"html")
            nombrePNG = auxiliar_ficheros.formatoArchivo("MapaDensidad_instante" + str(self.instanteActual), "png")
            fig.write_html(join(Constantes.RUTA_SALIDA,nombreHTML), auto_open=False)
            fig.write_image(join(Constantes.RUTA_SALIDA,nombrePNG))


    def realizarVideoHeatmap(self,indice_inicio,indice_final,rutaSalida = ""):

        # Genera los frames del video
        listaImagenes = []

        for i in range(indice_inicio,indice_final+1):##Check this.

            fig = self.__getMapFigure(i,Constantes.ZOOM_MAPAS_PLOT_VIDEO)
            # Agrega el frame actual al video
            fig_bytes = fig.to_image(format='png')
            listaImagenes.append(np.array(Image.open(io.BytesIO(fig_bytes))))
            print("añadido imagen numero : " + str(i))

        if rutaSalida == "":
            video_path = os.path.join("../", 'video.mp4')
        else:
            video_path = rutaSalida
        fps = 1
        codec = 'libx264'
        imageio.mimsave(video_path, listaImagenes, fps=fps, codec=codec)


