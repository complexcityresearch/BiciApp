import os
from os.path import join


import pandas as pd

from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros
from Backend.EstructurasDatos.data_matrix import Data_matrix, Desplazamientos_matrix


def cargarAntiguaEjecucion(directorio = "",coordendas = ""):

    path = join(os.getcwd(), "Soluciones")
    terminacion = "_Resultado.csv"

    listaDataFrame = []
    shapes = []

    if directorio == "":
        for matriz in Constantes.LISTA_MATRICES:
            direccionAbrir = join(path, matriz + terminacion)
            matriz = pd.read_csv(direccionAbrir)
            listaDataFrame.append(matriz)
            shapes.append(matriz.shape[1] - 1)
        Constantes.COORDENADAS = pd.read_csv(join(path, "COORDENADAS" + terminacion)).to_numpy()
    else:
        for direccion in directorio:
            matriz = pd.read_csv(direccion)
            listaDataFrame.append(matriz)
            shapes.append(matriz.shape[1] - 1)
        Constantes.COORDENADAS = pd.read_csv(coordendas).to_numpy()


    matrices = {

        Constantes.KMS_DEJAR_BICI: Data_matrix(shapes[3], listaDataFrame[3]),
        Constantes.KMS_COGER_BICI: Data_matrix(shapes[2], listaDataFrame[2]),
        Constantes.PETICIONES_NORESUELTAS_COGER_BICI: Data_matrix(shapes[6], listaDataFrame[6]),
        Constantes.PETICIONES_RESUELTAS_COGER_BICI: Data_matrix(shapes[4], listaDataFrame[4]),
        Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI: Data_matrix(shapes[7], listaDataFrame[7]),
        Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI: Data_matrix(shapes[5], listaDataFrame[5]),
        Constantes.OCUPACION: Data_matrix(shapes[0], listaDataFrame[0]),
        Constantes.DESPLAZAMIENTOS: Desplazamientos_matrix(listaDataFrame[14]),
        Constantes.OCUPACION_RELATIVA: Data_matrix(shapes[1], listaDataFrame[1]),
        Constantes.KMS_FICTICIOS_COGER: Data_matrix(shapes[8], listaDataFrame[8]),
        Constantes.KMS_FICTICIOS_DEJAR: Data_matrix(shapes[9], listaDataFrame[9]),
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI: Data_matrix(shapes[10], listaDataFrame[10]),
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI: Data_matrix(shapes[11], listaDataFrame[11]),
        Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI: Data_matrix(shapes[12], listaDataFrame[12]),
        Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI: Data_matrix(shapes[13], listaDataFrame[13]),

    }
    return matrices

def cargarMatrizCustom(direccion):
    matriz = pd.read_csv(direccion)
    return Data_matrix(matriz.shape[1]-1, matriz)

def cargarDatosParaSimular(rutaEntrada):

    ficheros_distancia = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada,
                                                                  ["indices_andar", "kms_andar",
                                                                   "indices_bicicleta",
                                                                   "kms_bicicleta"])

    if ficheros_distancia == []:
        ficheros = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada,
                                                            ["deltas", "capacidad", "indices", "kms", "coordenadas",
                                                             "tendencia"])
    else:
        ficheros = [None] * 8
        ficheros[0] = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["deltas"])[0]
        ficheros[1] = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["capacidad"])[0]
        ficheros[4] = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["coordenadas"])[0]
        ficheros[5] = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["tendencia"])[0]

    return ficheros,ficheros_distancia


def cargarSimulacionesParaAnalisis(pathEntrada):
    # Cargar variables de stress,costeAndar y delta para poder nombrar a los ficheros.
    rutas_matrices_analizar = auxiliar_ficheros.buscar_archivosEntrada(pathEntrada, Constantes.LISTA_MATRICES)
    ruta_resumen_ejecucion = auxiliar_ficheros.buscar_archivosEntrada(pathEntrada, ['Resumen'])
    ruta_fichero_coordenadas = auxiliar_ficheros.buscar_archivosEntrada(pathEntrada, ['coordenadas'])
    ruta_fichero_matrizCustom = auxiliar_ficheros.buscar_archivosEntrada(pathEntrada, ['Custom'])

    with open(ruta_resumen_ejecucion[0], "r") as archivo:
        contenido = archivo.read()
    contenido = contenido.split(",")

    if ruta_fichero_matrizCustom != []:  # Comprobar esto.
        Constantes.MATRIZ_CUSTOM = cargarMatrizCustom(ruta_fichero_matrizCustom[0])

    matrices = cargarAntiguaEjecucion(directorio=rutas_matrices_analizar,
                                                            coordendas=ruta_fichero_coordenadas[0])
    return matrices,contenido

#deprecated
def guardarArchivosEjecucion(matrices):
    path = join(os.getcwd(), "Soluciones")
    terminacion = "_Resultado.csv"
    matrices[Constantes.OCUPACION].matrix.to_csv(join(path, Constantes.OCUPACION + terminacion), index=False)
    matrices[Constantes.OCUPACION_RELATIVA].matrix.to_csv(join(path, Constantes.OCUPACION_RELATIVA + terminacion),
                                                          index=False)
    matrices[Constantes.KMS_FICTICIOS_COGER].matrix.to_csv(join(path, Constantes.KMS_FICTICIOS_COGER + terminacion),
                                                           index=False)
    matrices[Constantes.KMS_FICTICIOS_DEJAR].matrix.to_csv(join(path, Constantes.KMS_FICTICIOS_DEJAR + terminacion),
                                                           index=False)

    matrices[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI + terminacion), index=False)
    matrices[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI + terminacion), index=False)
    matrices[Constantes.DESPLAZAMIENTOS].matrix.to_csv(join(path, Constantes.DESPLAZAMIENTOS + terminacion),
                                                       index=False)
    matrices[
        Constantes.PETICIONES_RESUELTAS_COGER_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_RESUELTAS_COGER_BICI + terminacion), index=False)
    matrices[
        Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI + terminacion), index=False)
    matrices[
        Constantes.PETICIONES_NORESUELTAS_COGER_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_NORESUELTAS_COGER_BICI + terminacion), index=False)
    matrices[
        Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI + terminacion), index=False)
    matrices[Constantes.KMS_DEJAR_BICI].matrix.to_csv(join(path, Constantes.KMS_DEJAR_BICI + terminacion), index=False)
    matrices[Constantes.KMS_COGER_BICI].matrix.to_csv(join(path, Constantes.KMS_COGER_BICI + terminacion), index=False)

    pd.DataFrame(Constantes.COORDENADAS).to_csv(join(path, "COORDENADAS" + terminacion), index=False)

    matrices[
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI + terminacion), index=False)
    matrices[
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI].matrix.to_csv(
        join(path, Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI + terminacion), index=False)


