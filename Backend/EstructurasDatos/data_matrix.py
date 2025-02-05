import numpy as np
import pandas as pd

from Backend import Constantes


# Clase encargada de la construcción de las matrices necesarias para la tarea 1.
class Data_matrix:

    def __init__(self, n, dataframe: pd.DataFrame = None):

        columnas = ['UTempDelta'] + ['estacion' + str(i) for i in range(n)]

        if dataframe is None or dataframe.empty:
            self.matrix = pd.DataFrame(columns=columnas)
        else:
            dataframe.columns = columnas
            self.matrix = dataframe

        self.n = n
        self.lista = []


    def add_row(self, row: list):
        self.lista.append(row)

    def create_Dataframe(self):
        self.matrix = pd.DataFrame(self.lista,
                                   columns=['UTempDelta'] + ['estacion' + str(i) for i in range(self.n)])

    def add_row_position(self, position: int, row: list):
        if (len(self.lista) > position):
            self.lista[position] = row
        else:
            self.add_row(row)

    def colapsarEnUTempDelta(self):
        self.matrix = self.matrix.groupby("UTempDelta", as_index=False).sum()


class Desplazamientos_matrix:
    def __init__(self,dataframe:pd.DataFrame=None):
        self.columnas = ['Estacion origen', 'Estacion final', 'tipo de peticion', 'Utemporal', 'Cantidad_peticiones','RealFicticio']
        if dataframe is None or dataframe.empty:
            self.matrix = pd.DataFrame(
                columns=self.columnas)
        else:
            dataframe.columns = self.columnas
            self.matrix = dataframe
        self.lista = []

    def add_row(self, row: list):
        self.lista.append(row)

    def create_Dataframe(self):
        self.matrix = pd.DataFrame(self.lista,
                                   columns=self.columnas)

    def getCantidadPeticiones(self, fila: int):
        return self.matrix.iloc[fila, Constantes.MATRIZDESPLAZAMIENTOS_PETICIONES]

    def getUTemporal(self, fila: int):
        return self.matrix.iloc[fila, Constantes.MATRIZDESPLAZAMIENTOS_UTEMPORAL]


class Ocupacion_Horas:

    def __init__(self, matrizOcupacion: pd.DataFrame):
        delta_horas = (60 / Constantes.DELTA_TIME)

        matrizOcupacion.index = np.arange(0, len(matrizOcupacion))
        self.matrix = matrizOcupacion.groupby(matrizOcupacion.index // delta_horas).sum() / (60 / Constantes.DELTA_TIME)
        self.matrix = self.matrix.drop(self.matrix.columns[[0]], axis=1)
        self.matrix.insert(0, 'hora', range(0, len(self.matrix)))
