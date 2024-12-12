import math

import numpy
import numpy as np
import pandas as pd

from Backend import Constantes


def realizarMediaPesos(lista:list):

    np_lista = np.array(lista)
    sumaTotal = np_lista.sum()

    return (np_lista/sumaTotal).tolist()

def rellenarCon0(matriz:numpy.ndarray):

    dias = matriz.shape[0] / (24 * (60 / Constantes.DELTA_TIME))

    if not dias.is_integer():
        print(
            "IT HAS BEEN DETECTED THAT THE DELTAS PRESENTED ARE MISSING SOME DELTA LINES, FILLING AT THE END OF THE FILE WITH 0...")
        peticionesNecesarias = (math.trunc(dias) + 1) * 24 * (60 / Constantes.DELTA_TIME)

        for i in range(int(abs(matriz.shape[0] - peticionesNecesarias))):
            # Obtener la forma actual del array
            filas, columnas = matriz.shape

            # Crear una fila de ceros
            fila_ceros = np.zeros((1, columnas))

            # Apilar la fila de ceros al final del array
            matriz = np.vstack((matriz, fila_ceros))
        dias = matriz.shape[0] / (24 * (60 / Constantes.DELTA_TIME))
        if not dias.is_integer():
            raise Exception("ERROR WHEN INSERTING NEW DELTAS.")
    return matriz

#FUncion a llamar antes de realizar la compresion en deltas
def rellenarFilasMatrizDeseada(matriz:pd.DataFrame,deltasMax):
    nuevaMatriz = matriz.set_index(matriz.columns[0])
    nuevaMatriz = nuevaMatriz.reindex(range(deltasMax+1), fill_value=0)
    nuevaMatriz = nuevaMatriz.reset_index()
    return nuevaMatriz

