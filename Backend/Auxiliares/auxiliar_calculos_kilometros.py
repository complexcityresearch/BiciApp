import numpy as np
import pandas as pd

from Backend import Constantes


#Función encargada de transformar una matriz de kms (coger o salir) de periodos de unidades delta a horas.
#La dificultad se encuentra ya que hay tramos donde, al no recorrer ningún kilómetro, tenemos que obviarlos.
def getDfKmsHorarios(matriz:pd.DataFrame):

    #Calculamos cuantas deltas hay en una hora:
    deltaHoras = 60 / Constantes.DELTA_TIME
    #Para saber a que hora corresponde cada Utempdelta podemos realizar lo siguiente:
    # Podemos tomar el valor Utempdelta/4 y truncar el resultado, de forma que, obtendremos la hora correspondiente a
    #la que pertenece.

    np_matriz = matriz.to_numpy()
    np_matriz[:, 0] = np.trunc(np_matriz[:, 0] / deltaHoras)

    #Acto seguido, podemos sumar las horas que sean iguales, ya que es el mismo periodo.
    return pd.DataFrame(np_matriz,columns=matriz.columns).groupby("UTempDelta").sum().reset_index(level=0)
