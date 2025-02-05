import numpy as np
import pandas as pd


def filtrarEstaciones(datos:pd.DataFrame,lista_estaciones,listaCoordenadas:np.numarray):
    datosSinHoras = datos.iloc[:, 1:]
    datosFiltrados = datosSinHoras.iloc[:, lista_estaciones]
    datosFiltrados.insert(0, 'UTemp', datos.iloc[:, 0])
    datos = datosFiltrados
    coordenadas = listaCoordenadas[lista_estaciones, :]
    coordenadaCentro = (coordenadas[0, 1], coordenadas[0, 2])

    return datos,coordenadas,coordenadaCentro