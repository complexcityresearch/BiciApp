import os
from os.path import join

import numpy as np
import pandas as pd

from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion
from Backend.Representacion.Mapas.Voronoi import VoronoiPersonalizado


class manejar_Voronoi(Interfaz_Representacion):

    def __init__(self,matriz:pd.DataFrame,coordenadas:np.array,escalaPositivos=None,escalaNegativos=None):
        self.matriz = matriz
        self.coordenadas = coordenadas
        self.escalaPositivos = escalaPositivos
        self.escalaNegativos = escalaNegativos

    def __inicializarMapaVoronoi(self):
        voronoi = VoronoiPersonalizado(self.coordenadas,paletaPositiva=self.escalaPositivos,paletaNegativa=self.escalaNegativos)
        voronoi.calcularVoronoi()
        return voronoi

    def cargarMapaInstante(self, instante,listaEstaciones=None,accion=None,tipo=None):
        voronoi = self.__inicializarMapaVoronoi()
        voronoi.cargarColoresOcupacion(self.matriz, instante)
        voronoi.representarVoronoi(instante)

    def getFichero(self):
        return join(os.getcwd(),"MapaVoronoi.html")


    def getInstanciasMax(self):
        return str(self.matriz.shape[0])

