import numpy as np
import pandas as pd


#Función encargada de sumar las matrices. El único requisito es que las matrices tengan el mismo delta.
#Realiza la suma por la unidad temporal y no por el indice de la matriz.
def agruparMatrices(matriz1:pd.DataFrame,matriz2:pd.DataFrame):

    if matriz1.empty:
        return matriz2
    else:
        if matriz2.empty:
            return matriz1

    nuevoDataFrame = matriz1.to_numpy().copy()

    listaDeltasMatriz1 = matriz1.iloc[:,0].to_numpy()

    for i in range(matriz2.shape[0]):
        delta = matriz2.iloc[i,0]

        filtradoIndices = listaDeltasMatriz1 == delta

        if filtradoIndices.any():#En el caso de que exista el delta.

            indiceDelta = np.where(filtradoIndices == True)[0][0]
            nuevoDataFrame[indiceDelta,1:] = nuevoDataFrame[indiceDelta,1:] + matriz2.iloc[i,1:]
        else:#En el caso de que no exista, introduciremos la fila de la segunda matriz.

            nuevoDataFrame = np.vstack([nuevoDataFrame,matriz2.iloc[i,:].to_numpy().copy()])
            indices = np.argsort(nuevoDataFrame[:, 0])

            # Reordenamos el array en función de los valores de la segunda columna
            nuevoDataFrame = nuevoDataFrame[indices]

    return pd.DataFrame(nuevoDataFrame,columns=matriz1.columns)


def sustraerMatrices(matriz1:pd.DataFrame,matriz2:pd.DataFrame):
    if matriz1.empty:
        matriz2.iloc[:, 1:] = -matriz2.iloc[:, 1:]
        return matriz2
    else:
        if matriz2.empty:
            return matriz1

    nuevoDataFrame = matriz1.to_numpy().copy()

    listaDeltasMatriz1 = matriz1.iloc[:,0].to_numpy()

    for i in range(matriz2.shape[0]):
        delta = matriz2.iloc[i,0]

        filtradoIndices = listaDeltasMatriz1 == delta

        if filtradoIndices.any():#En el caso de que exista el delta.

            indiceDelta = np.where(filtradoIndices == True)[0][0]
            nuevoDataFrame[indiceDelta,1:] = nuevoDataFrame[indiceDelta,1:] - matriz2.iloc[i,1:]
        else:#En el caso de que no exista, introduciremos la fila de la segunda matriz.
            fila = matriz2.iloc[i,:].to_numpy()
            fila[1:] = -fila[1:]
            nuevoDataFrame = np.vstack([nuevoDataFrame,fila])
            indices = np.argsort(nuevoDataFrame[:, 0])

            # Reordenamos el array en función de los valores de la segunda columna
            nuevoDataFrame = nuevoDataFrame[indices]

    return pd.DataFrame(nuevoDataFrame,columns=matriz1.columns)




#Funcion encargada de colapsar una matriz y pasar de un delta a otro.
def colapsarDeltasMedia(matriz:pd.DataFrame,deltaActual,deltaDeseado):

    colapsarCadaDelta = deltaDeseado / deltaActual #Numero de deltas a colapsar.

    matrizColapsada = matriz.iloc[:,1:].groupby(matriz.index // colapsarCadaDelta).sum()/colapsarCadaDelta
    matrizColapsada.insert(0, "UTemporal", range(matrizColapsada.shape[0]), True)
    return matrizColapsada

#np.logical_and(Agrupador.colapsarDeltasMedia(matrices[Constantes.OCUPACION].matrix, 15, 60).iloc[:,1:].to_numpy(),matrices[Constantes.OCUPACION_HORAS].matrix.iloc[:,1:].to_numpy())
def colapsarDeltasAcumulacion(matriz:pd.DataFrame,deltaActual,deltaDeseado):
    colapsarCadaDelta = deltaDeseado / deltaActual  # Numero de deltas a colapsar.
    matrizColapsada = matriz.iloc[:, 1:].groupby(matriz.index // colapsarCadaDelta).sum()
    matrizColapsada.insert(0, "UTemporal", range(matrizColapsada.shape[0]), True)
    return matrizColapsada

def colapsarDesplazamientos(matrizDesplazamientos:pd.DataFrame,deltaActual,deltaDeseado):

    colapsarCadaDelta = deltaDeseado / deltaActual
    matrizDesplazamientos.iloc[:,3] = matrizDesplazamientos.iloc[:,3]//colapsarCadaDelta #Reorienta los indexes.
    columnas = matrizDesplazamientos.columns.to_list()

    nuevaMatriz =  matrizDesplazamientos.groupby([columnas[0], columnas[1], columnas[2], columnas[3], columnas[5]]).agg({columnas[4]: 'sum'}).reset_index().sort_values(columnas[3], ascending=True)


    nuevaMatriz = nuevaMatriz[columnas]
    return nuevaMatriz