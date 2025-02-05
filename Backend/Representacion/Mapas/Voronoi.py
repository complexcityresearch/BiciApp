
from os.path import join

import branca
import folium
import numpy as np
import pandas as pd
from geovoronoi import voronoi_regions_from_coords
from shapely.geometry import Polygon

from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros
from Backend.EstructurasDatos.Poligonos import Poligonos
import seaborn as sns

class VoronoiPersonalizado:

    def __init__(self, coordenadas,paletaPositiva=None,paletaNegativa=None):
        self.coordenadas = coordenadas
        self.mapa = folium.Map([coordenadas[172][1],coordenadas[172][2]], zoom_start=13)
        self.arrayPoligonos: list[Poligonos] = []
        self.paletaPositiva = paletaPositiva
        self.paletaNegativa = paletaNegativa

    #Funcion que calcula las regiones de Voronoi
    def calcularVoronoi(self):
        maxLat = self.coordenadas[:, 1].max()
        maxLong = self.coordenadas[:, 2].max()
        minLat = self.coordenadas[:, 1].min()
        minLong = self.coordenadas[:, 2].min()

        folium.Polygon([(minLat, maxLong), (maxLat, maxLong), (maxLat, minLong), (minLat, minLong)],
                       color="blue").add_to(self.mapa)

        region_polys, region_pts = voronoi_regions_from_coords(self.coordenadas[:,1:], geo_shape=Polygon([(minLat, maxLong), (maxLat, maxLong), (maxLat, minLong), (minLat, minLong)]))

        for i in range(len(region_polys)):
            poligono = region_polys[i].boundary.coords[:]
            self.arrayPoligonos.append(Poligonos(region_pts[i], poligono))

            # folium.Polygon(poligono, color="blue", fill=True, fill_color="orange", fill_opacity=0.4).add_to(self.mapa)


    def elegirPaletas(self,opcion,nValores):
        if opcion == "Escala de verdes":
            green_values = np.linspace(1, 0.1, nValores)
            gv = green_values.copy()
            gv = np.flip(gv)
            paleta_negativos = sns.color_palette([(0, r, 0) for r in gv]).as_hex()

            return paleta_negativos
        if opcion == "Magma":
            paleta = sns.color_palette("magma", nValores).as_hex()
            return paleta
        if opcion == "Círculo de colores":
            return sns.color_palette("hls", 8).as_hex()

    #PREGUNTAR SI LOS COLORES LOS QUIERE CON RESPECTO AL TOTAL O LA HORA EN SÍ.
    def cargarColoresOcupacion(self,ocupaciones:pd.DataFrame,index):
        np_ocupaciones = np.array(ocupaciones.iloc[:,1:])
        valorMax = np_ocupaciones[index].max()
        valorMin = np_ocupaciones[index].min()
        #array_indices_menorAmayor = np.argsort(np_ocupaciones)
        nValoresPos = len(np.unique(ocupaciones[ocupaciones>=0]))
        nValoresNeg = len(np.unique(ocupaciones[(ocupaciones <0)]))



        # Crear la paleta personalizada
        if valorMin < 0:

            if self.paletaNegativa == None:
                green_values = np.linspace(1, 0.1, nValoresNeg)
                gv = green_values.copy()
                gv= np.flip(gv)
                paleta_negativos = sns.color_palette([(0, r, 0) for r in gv]).as_hex()
                neg_palete = sns.color_palette([(0, r, 0) for r in green_values],as_cmap=True)
                neg_cmap = branca.colormap.LinearColormap(
                    colors=[neg_palete[x] for x in range(nValoresNeg)],
                    vmin=valorMin, vmax=0
                )
                colormap = neg_cmap.scale(valorMin, 0)
                colormap = colormap.to_step(n=4)
                colormap.caption = 'Negative data represented'
                colormap.add_to(self.mapa)
            else:
                paleta_negativos = self.elegirPaletas(self.paletaNegativa,nValoresNeg)

                arrayColores = []
                for x in range(len(paleta_negativos)):

                    arrayColores.append(paleta_negativos[x])
                arrayColores.reverse()
                #neg_palete.reverse()

                neg_cmap = branca.colormap.LinearColormap(
                    colors=arrayColores,
                    vmin=valorMin, vmax=0
                )
                colormap = neg_cmap.scale(valorMin, 0)
                colormap = colormap.to_step(n=4)
                colormap.caption = 'Negative data represented'
                colormap.add_to(self.mapa)

        if valorMax > 0:

            if self.paletaPositiva == None:
                paleta = sns.color_palette("magma",len(np.unique(ocupaciones[ocupaciones>=0]))).as_hex()
                magma_palette = sns.color_palette("magma", as_cmap=True)
                magma_cmap = branca.colormap.LinearColormap(
                    colors=[magma_palette(x) for x in range(256)],
                    vmin=0, vmax=valorMax
                )
                colormap = magma_cmap.scale(0, valorMax)
                colormap = colormap.to_step(n=4)
                colormap.caption = 'Data represented'
                colormap.add_to(self.mapa)
            else:
                paleta=self.elegirPaletas(self.paletaPositiva, nValoresPos)


                magma_cmap = branca.colormap.LinearColormap(
                    colors=[paleta[x] for x in range(len(paleta))],
                    vmin=0, vmax=valorMax
                )
                colormap = magma_cmap.scale(0, valorMax)
                colormap = colormap.to_step(n = 4)
                colormap.caption = 'Data represented'
                colormap.add_to(self.mapa)

        #End prueba


        for i in self.arrayPoligonos:
            valorPunto = np_ocupaciones[index,i.indicePunto][0]
            i.ocupacion = valorPunto
            if valorPunto < 0:
                #i.color = '#ff0000'
                i.color = paleta_negativos[round(abs(valorPunto) * (len(paleta_negativos) - 1) / abs(valorMin))]
            else:
                if valorMax > 0:
                    i.color = paleta[round(valorPunto * (len(paleta)-1) / valorMax)]
                else:
                    i.color = '#000000'

    #Funcion encargada de representar el diagrama, haya o no colores
    def representarVoronoi(self,instante):
        self.representacionBasica()
        for i in self.arrayPoligonos:

            if i.color == None:
                folium.Polygon(i.poligono, color="blue", fill=False,popup=str("Station" + str(i.indicePunto))).add_to(self.mapa)
            else:
                folium.Polygon(i.poligono,color="black", fill=True, fill_color=i.color, fill_opacity=0.6,popup=str("Station" + str(i.indicePunto) +"\n" + "Data: " + str(i.ocupacion)) ).add_to(
                    self.mapa)

        if Constantes.RUTA_SALIDA != "":
            nombre = auxiliar_ficheros.formatoArchivo("MapaVoronoi_instante"+str(instante),"html")

            self.mapa.save("MapaVoronoi.html")
            self.mapa.save(join(Constantes.RUTA_SALIDA,nombre))
            
        else:
            self.mapa.save("MapaVoronoi.html")

    # Función que representa un mapa con círculos que representan las estaciones.
    def representacionBasica(self):

        for i in range(len(self.coordenadas)):
            self.__dibujarCirculo(self.coordenadas[i][1], self.coordenadas[i][2], 50, "red",
                                  "Station " + str(i))
        #self.mapa.save("mapa.html")

    # Función auxiliar que representa un circulo dado sus coordenadas, el radio y el color deseado.
    def __dibujarCirculo(self, lat, long, radio, color, label="error"):
        folium.Circle(
            radius=radio,
            location=[lat, long],
            color=color,
            fill=True
        ).add_child(folium.Popup(label)).add_to(self.mapa)
