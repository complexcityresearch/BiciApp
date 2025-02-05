import os
from os.path import join

import numpy as np
import pandas as pd

from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion
from Backend.Representacion.Mapas.MapaDesplazamientos import MapaDesplazamientos


class Manejar_Desplazamientos(Interfaz_Representacion):

    def __init__(self,matriz:pd.DataFrame,coordenadas:np.array,listaEstaciones=None,accion=None,tipo=None):
        self.matriz = matriz
        self.coordenadas = coordenadas
        self.listaEstaciones = listaEstaciones
        self.accion = accion
        self.tipo = tipo


    def cargarMapaInstante(self, instante,listaEstaciones=None,accion=None,tipo=None):

        md = MapaDesplazamientos(self.coordenadas,self.matriz)
        md.representarInstante(instante,self.accion,self.tipo)


    def getFichero(self):
        return join(os.getcwd(),"MapaDesplazamientos.html")


    def getInstanciasMax(self):
        return str(self.matriz.shape[0])