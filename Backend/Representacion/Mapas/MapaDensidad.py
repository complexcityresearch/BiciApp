import io
import os

from os.path import join

import imageio
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros


#Clase para la representacion con folium
class MapaDensidad2:

    def __init__(self,coordenadas:np.ndarray):
        self.datos = pd.DataFrame()
        self.coordenadas = pd.DataFrame(coordenadas,columns=["Estacion","Lat","Long"])
        self.coordenadaCentro = (coordenadas[172,1],coordenadas[172,2])


    def cargarDatos(self, datos:pd.DataFrame, lista_estaciones=None):
        if lista_estaciones == None:
            self.datos= datos
        else:#En el caso de que el usuario desee, ser capaz de representar SOLO las estaciones deseadas.
            datosSinHoras = datos.iloc[:,1:]
            if lista_estaciones != []:
                datosFiltrados = datosSinHoras.iloc[:,lista_estaciones]
            else:
                datosFiltrados = datosSinHoras
            datosFiltrados.insert(0, 'UTemp',datos.iloc[:,0] )
            self.datos = datosFiltrados
            if lista_estaciones != []:
                self.coordenadas = self.coordenadas.iloc[lista_estaciones,:]

            self.coordenadaCentro = (self.coordenadas.iloc[self.coordenadas.shape[0]//2,1],self.coordenadas.iloc[self.coordenadas.shape[0]//2,2])


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


        fig = px.density_mapbox(datos, lat="Lat", lon="Long", z="Datos", radius=50,
                                center=dict(lat=self.coordenadaCentro[0], lon=self.coordenadaCentro[1]),
                                zoom=zoom,
                                mapbox_style="open-street-map",
                                hover_data={'Estacion': True},
                                opacity=opacidad,
                                range_color=(valorMin,valorMax))

        fig.update_layout(mapbox=dict(center=dict(lat=self.coordenadaCentro[0], lon=self.coordenadaCentro[1]), zoom=zoom),
                          width=1200, height=1200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def representarHeatmap(self, instante):

        fig = self.__getMapFigure(instante,Constantes.ZOOM_MAPAS_PLOT)
        if Constantes.RUTA_SALIDA == "":
            fig.write_html("MapaDensidad.html",auto_open=False)
            #fig.show()
        else:
            nombreHTML = auxiliar_ficheros.formatoArchivo("MapaDensidad_instante"+str(instante),"html")
            nombrePNG = auxiliar_ficheros.formatoArchivo("MapaDensidad_instante" + str(instante), "png")
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


