import os
from os.path import join

import numpy as np
import pandas as pd

from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion
from Backend.Representacion.Mapas.MapaDensidad import MapaDensidad2


class Manejar_Densidad(Interfaz_Representacion):

    def __init__(self,matriz:pd.DataFrame,coordenadas:np.array,listaEstaciones=None):
        self.matriz = matriz
        self.coordenadas = coordenadas
        self.listaEstaciones = listaEstaciones


    def cargarMapaInstante(self, instante,listaEstaciones=None,accion=None,tipo=None):
        md = MapaDensidad2(self.coordenadas)
        md.cargarDatos(self.matriz,lista_estaciones=self.listaEstaciones)
        md.representarHeatmap(instante)


    def getFichero(self):
        return join(os.getcwd(),"MapaDensidad.html")


    def getInstanciasMax(self):
        return str(self.matriz.shape[0])