import os
from os.path import join

import numpy as np
import pandas as pd

from Backend.Auxiliares import auxiliar_estaciones
from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion
from Backend.Representacion.Mapas.MapaCirculos import MapaCirculos


class manejar_mapaCirculos(Interfaz_Representacion):

    def __init__(self,matriz:pd.DataFrame,coordenadas:np.array,mostrarLabels = False,listaEstaciones=None,accion=None,tipo=None):
        self.matriz = matriz
        self.coordenadas = coordenadas
        self.mostrarLabels = mostrarLabels
        self.listaEstaciones = listaEstaciones
        self.accion = accion
        self.tipo = tipo


    def cargarMapaInstante(self, instante,listaEstaciones=None,accion=None,tipo=None):
        if self.listaEstaciones != None:
            valorMax = int(self.matriz.iloc[:,1:].max().max())
            datos,coordenadas,coordenadaCentro=auxiliar_estaciones.filtrarEstaciones(self.matriz,lista_estaciones=self.listaEstaciones,listaCoordenadas=self.coordenadas)
        else:
            datos = self.matriz
            coordenadas = self.coordenadas
            valorMax = None

        mc=MapaCirculos(datos,coordenadas,valorMax=valorMax,mostrarPopup=self.mostrarLabels)
        mc.representarInstante(instante)


    def getFichero(self):
        return join(os.getcwd(),"MapaCirculos.html")


    def getInstanciasMax(self):
        return str(self.matriz.shape[0])
