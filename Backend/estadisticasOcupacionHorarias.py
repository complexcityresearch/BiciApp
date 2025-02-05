import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

from Backend import Constantes
from Backend.Auxiliares import auxiliar_representacion, auxiliar_tiempo
from Backend.Manipuladores import Agrupador


class estadisticasOcupacionHorarias:

    def __init__(self, matrizOcupacionHoraria: pd.DataFrame, deltaTime: int,crearFigure = True):
        self.matrizOcupacionHoraria = matrizOcupacionHoraria
        self.nombreTiempo = matrizOcupacionHoraria.columns[0]
        self.engine = create_engine('sqlite://', echo=False)
        self.matrizOcupacionHoraria.to_sql('ocupacionesHoras', con=self.engine)
        self.deltaTime = deltaTime
        if crearFigure:
            self.figure = plt.figure()

    # Funcion dado una estacion y un rango de dias, muestra un histograma con los datos de ocupación media en varios dias.
    def HistogramaPorEstacion(self, estacion: int, dias: list[int], nombreGrafica=""):
        lista_horas = self.getInformacionDiaEnHorasEstacion(estacion, dias)
        auxiliar_representacion.pintarGraficaBarras(lista_horas, range(0, 24), nombreGrafica=nombreGrafica)

    # Función que dado un rango de dias muestra el histograma con las ocupaciones medias de cada día de todas las estaciones.
    def HistogramaOcupacionMedia(self, dias: list[int],listaEstaciones:list = None, nombreGrafica="",frecuencia = True,media=True):
        lista_estaciones = self.getOcupacionTodasEstaciones(dias,listaEstaciones=listaEstaciones,media=media)
        n = self.matrizOcupacionHoraria.shape[1] - 1
        if frecuencia:
            auxiliar_representacion.histogramaFrecuencia(lista_estaciones,nombreGrafica=nombreGrafica)
        else:
            #auxiliar_representacion.pintarGraficaBarras(lista_estaciones, range(0, n), nombreGrafica=nombreGrafica)
            auxiliar_representacion.pintarGraficaBarrasEstaciones(lista_estaciones,range(0,n), nombreGrafica=nombreGrafica)

    def HistogramaAcumulacion(self, estacion, dias: list[int], nombreGrafica=""):
        lista_horas = np.array([0] * 24)
        for i in range(len(dias)):
            lista_aux = self.getInformacionDiaEnHorasEstacion(estacion, [dias[i]])
            lista_horas = lista_horas + lista_aux
        auxiliar_representacion.pintarGraficaBarras(lista_horas.tolist(), range(0, 24), nombreGrafica=nombreGrafica)

    # Función dado una estación y un dia determinado lo muestra en un histograma de lineas la trayectoria de la ocupación
    # del día, permitiendo comparar varias estaciones y varios días a la vez.
    # Estaciones-> Array de estaciones a comparar.
    # Dias -> Array que contiene los arrays de dias para realizar la comparación.
    # El array Estaciones y el Array de Días DEBEN de tener el mismo tamaño
    def HistogramaCompararEstaciones(self, estaciones: list[int], diasPorEstacion: list[list[int]], media=True,
                                     nombreGrafica=""):

        listaHistogramas = []  # Array de los n histogramas.
        listaNombres = []
        for i in range(len(estaciones)):  # Para cada estación conseguimos su histograma.
            listaHistogramas.append(self.getInformacionDiaEnHorasEstacion(estaciones[i], diasPorEstacion[i], media))
            # listaNombres.append("Estacion " + str(estaciones[i]) + " en los dias: " + str(diasPorEstacion[i]))
            nombre = "Station " + str(estaciones[i])
            if len(diasPorEstacion[i]) <= 4:
                nombre += " in day " + str(diasPorEstacion[i])
            listaNombres.append(nombre)

        auxiliar_representacion.pintarVariosHistogramas(listaHistogramas, listaNombres, nombreGrafica=nombreGrafica)

    # Funcion usada para ver comparaciones entre días laborables y festivos.
    # Toma una nueva matriz por parámetro para realizar la comparación, deben de tener el mismo delta, si no, la comparacion
    # carace de sentido alguno.
    def HistogramaCompararMatrices(self, matrizComparacion: pd.DataFrame,delta_matrizComparacion, estaciones1: list[int],
                                   estaciones2: list[int], media=True,
                                   nombreGrafica=""):

        listaHistogramas = []  # Array de los n histogramas.
        listaNombres = []

        if delta_matrizComparacion != 60:
            if media:
                matrizComparacion = Agrupador.colapsarDeltasMedia(Constantes.MATRIZ_CUSTOM.matrix,delta_matrizComparacion,60)
            else:
                matrizComparacion = Agrupador.colapsarDeltasAcumulacion(Constantes.MATRIZ_CUSTOM.matrix, delta_matrizComparacion, 60)
        delta_matrizComparacion = 60
        deltasDias1 = 24 * (60/self.deltaTime)
        deltasDias2 = 24

        dias1 = [list(range(0, int(self.matrizOcupacionHoraria.shape[0] / deltasDias1)))] * len(estaciones1)
        dias2 = [list(range(0,int(matrizComparacion.shape[0]/deltasDias2)))] * len(estaciones2)

        for i in range(len(estaciones1)):  # Para cada estación de nuestra matriz conseguimos el histograma
            listaHistogramas.append(self.getInformacionDiaEnHorasEstacion(estaciones1[i], dias1[i], media))
            listaNombres.append("Station " + str(estaciones1[i]) + " of matrix 1")

        for i in range(len(estaciones2)):  # Para cada estación conseguimos su histograma.
            listaHistogramas.append(self.__getOcupacionExterna(matrizComparacion,delta_matrizComparacion,estaciones2[i], dias2[i], media))
            listaNombres.append("Station " + str(estaciones2[i]) + " of matrix 2")

        auxiliar_representacion.pintarVariosHistogramas(listaHistogramas, listaNombres, nombreGrafica=nombreGrafica)

    # Función privada que realiza una consulta SQL para obtener las ocupaciones medias diarias de cada estación.
    def getOcupacionTodasEstaciones(self, dias: list[int],listaEstaciones=None ,media = True):
        n = self.matrizOcupacionHoraria.shape[1] - 1
        lista_estaciones = np.array([0] * n)

        for dia in dias:
            index_inicio_dia, index_final_dia = auxiliar_tiempo.diaToDelta(dia, dia, self.deltaTime)
            peticionSQL = self.engine.execute(
                "Select *  FROM ocupacionesHoras Where " + self.nombreTiempo + " between " + str(
                    index_inicio_dia) + " and " + str(index_final_dia)).fetchall()
            if media == True:
                lista_estaciones = lista_estaciones + np.sum(np.array(peticionSQL)[:, 2:], axis=0) / 24
            else:
                lista_estaciones = lista_estaciones + np.sum(np.array(peticionSQL)[:, 2:], axis=0)

        if media == True:
            lista_estaciones  = lista_estaciones / len(dias)

        if listaEstaciones != None:
            lista_estaciones = np.array(lista_estaciones)[listaEstaciones].tolist()

        return lista_estaciones

    # Función privada que realiza una consulta SQL para obtener las ocupaciones por horas de una estación indicada en un periodo
    # determinado.
    def getInformacionDiaEnHorasEstacion(self, estacion, dias: list[int], media=True):

        lista_horas = np.array([0] * 24)
        for dia in dias:
            index_inicio_dia, index_final_dia = auxiliar_tiempo.diaToDelta(dia, dia, self.deltaTime)
            peticionSQL = self.engine.execute(
                "Select estacion" + str(estacion) + " FROM ocupacionesHoras Where " + self.nombreTiempo + " between " +
                str(index_inicio_dia) + " and " + str(index_final_dia)).fetchall()

            lista_horas = lista_horas + np.transpose(np.array(peticionSQL))[0]
        if media:
            lista_horas = lista_horas / len(dias)

        return lista_horas

    # Funcion privada que realiza la consulta SQL a una matriz externa.

    def __getOcupacionExterna(self, matriz: pd.DataFrame,delta, estacion, dias: list[int], media=True):
        engineExterna = create_engine('sqlite://', echo=False)
        matriz.to_sql('matrizExterna', con=engineExterna)

        lista_horas = np.array([0] * 24)
        for dia in dias:
            index_inicio_dia, index_final_dia = auxiliar_tiempo.diaToDelta(dia, dia, delta)
            peticionSQL = engineExterna.execute(
                "Select estacion" + str(estacion) + " FROM matrizExterna Where " + matriz.columns[0] + " between " +
                str(index_inicio_dia) + " and " + str(index_final_dia)).fetchall()
            lista_horas = lista_horas + np.transpose(np.array(peticionSQL))[0]
        if media:
            lista_horas = lista_horas / len(dias)

        return lista_horas
