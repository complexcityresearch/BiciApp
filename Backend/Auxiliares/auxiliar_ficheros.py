import datetime
import os
import re
from os.path import join

from Backend import Constantes
from Backend.EstructurasDatos.data_matrix import Data_matrix


def formatoArchivo(nombreArchivo, extension):
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S") + "_" + nombreArchivo + "D"+str(Constantes.DELTA_TIME) +"S"+str(Constantes.PORCENTAJE_ESTRES) +"C"+str(Constantes.COSTE_ANDAR) + "." + extension


def buscar_archivosEntrada(ruta,nombresBuscar:list):
    ficheros = []

    archivos = os.listdir(ruta)

    for i in range(len(nombresBuscar)):

        for archivo in archivos:
            ruta_fichero = join(ruta, archivo)

            if re.search(r""+nombresBuscar[i],archivo):
                ficheros.append(ruta_fichero)

    return ficheros


def guardarMatricesEnFicheros(matrices: dict[str, Data_matrix], resumen: str,dirSalida):
    ruta = dirSalida
    for key in Constantes.LISTA_MATRICES:
        nombreArchivo = formatoArchivo(key + "_Resultado", "csv")
        pd_matriz = matrices[key].matrix
        pd_matriz.to_csv(join(ruta, nombreArchivo), index=False)

    nombreResumen = formatoArchivo("ResumenEjecucion", "txt")

    with open(join(ruta, nombreResumen), "w") as archivo:
        archivo.write(resumen)


def hacerResumenMatricesSalida(matrices: dict):
    Kms_coger = matrices[Constantes.KMS_COGER_BICI].matrix.iloc[:, 1:].sum().sum()
    Kms_dejar = matrices[Constantes.KMS_DEJAR_BICI].matrix.iloc[:, 1:].sum().sum()

    Kms_ficticios_coger = matrices[Constantes.KMS_FICTICIOS_COGER].matrix.iloc[:, 1:].sum().sum()
    Kms_ficticios_dejar = matrices[Constantes.KMS_FICTICIOS_DEJAR].matrix.iloc[:, 1:].sum().sum()

    N_Peticiones_Resueltas_coger = matrices[Constantes.PETICIONES_RESUELTAS_COGER_BICI].matrix.iloc[:,
                                   1:].sum().sum()
    N_Peticiones_Resueltas_dejar = matrices[Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI].matrix.iloc[:,
                                   1:].sum().sum()

    N_Peticiones_noResueltas_coger = matrices[Constantes.PETICIONES_NORESUELTAS_COGER_BICI].matrix.iloc[:,
                                     1:].sum().sum()
    N_Peticiones_noResueltas_dejar = matrices[Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI].matrix.iloc[:,
                                     1:].sum().sum()

    N_Peticiones_Resueltas_Ficticia_coger = matrices[Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI].matrix.iloc[:,
                                   1:].sum().sum()
    N_Peticiones_Resueltas_Ficticia_dejar = matrices[Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI].matrix.iloc[:,
                                   1:].sum().sum()



    N_Peticiones_Ficticias_noResueltas_coger = matrices[
                                                   Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI].matrix.iloc[
                                               :, 1:].sum().sum()
    N_Peticiones_Ficticias_noResueltas_dejar = matrices[
                                                   Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI].matrix.iloc[
                                               :, 1:].sum().sum()



    soluciones = {
        Constantes.KMS_COGER_BICI: Kms_coger,
        Constantes.KMS_DEJAR_BICI: Kms_dejar,
        Constantes.KMS_FICTICIOS_COGER: Kms_ficticios_coger,
        Constantes.KMS_FICTICIOS_DEJAR: Kms_ficticios_dejar,
        Constantes.PETICIONES_NORESUELTAS_COGER_BICI: N_Peticiones_noResueltas_coger,
        Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI: N_Peticiones_noResueltas_dejar,
        Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI: N_Peticiones_Ficticias_noResueltas_coger,
        Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI: N_Peticiones_Ficticias_noResueltas_dejar,
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI: N_Peticiones_Resueltas_Ficticia_coger,
        Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI: N_Peticiones_Resueltas_Ficticia_dejar,
        Constantes.PETICIONES_RESUELTAS_COGER_BICI: N_Peticiones_Resueltas_coger,
        Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI: N_Peticiones_Resueltas_dejar

    }

    cadena = \
        str(Constantes.DELTA_TIME) + ',' + str(Constantes.PORCENTAJE_ESTRES) + ',' +str(
            soluciones[Constantes.KMS_COGER_BICI]) +',' + str(
            soluciones[Constantes.KMS_DEJAR_BICI]) +',' + str(
            soluciones[Constantes.KMS_FICTICIOS_COGER]) +',' + str(
            soluciones[Constantes.KMS_FICTICIOS_DEJAR]) +',' + str(
            soluciones[Constantes.PETICIONES_RESUELTAS_COGER_BICI]) +',' + str(
            soluciones[Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI]) +',' + str(
            soluciones[Constantes.PETICIONES_NORESUELTAS_COGER_BICI]) +',' + str(
            soluciones[Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI]) +',' + str(
            soluciones[Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI]) + ',' + str(
            soluciones[Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI]) + ','   +str(
            soluciones[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI]) +',' + str(
            soluciones[Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI])

    return cadena

def guardarFicheroFiltrado(texto,tipo_filtrado,parametrosConsulta):
    nombreResumen = formatoArchivo("Filtrado_"+tipo_filtrado+"_"+parametrosConsulta,"txt")

    with open(join(Constantes.RUTA_SALIDA, nombreResumen), "w") as archivo:
        archivo.write(texto)