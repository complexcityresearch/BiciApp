from os.path import join

from matplotlib import pyplot as plt

from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros


def pintarGraficaBarras(lista_valores: list, rango: range, nombreGrafica ="Grafica"):

    ejeY = lista_valores
    ejeX = list(rango)

    plt.bar(ejeX,ejeY)
    plt.xlabel('Time (hours)')
    plt.ylabel('Values')
    plt.title('Bar chart')
    if Constantes.RUTA_SALIDA == "":
        plt.show()
    else:
        nombre = auxiliar_ficheros.formatoArchivo(nombreGrafica,"png")
        plt.savefig(join(Constantes.RUTA_SALIDA,nombre))

def pintarGraficaBarrasEstaciones(lista_valores: list, rango: range, nombreGrafica ="Grafica"):

    ejeY = lista_valores
    ejeX = list(rango)

    plt.bar(ejeX,ejeY)
    plt.xlabel('Stations')
    plt.ylabel('Values')
    plt.title('Bar chart')
    if Constantes.RUTA_SALIDA == "":
        plt.show()
    else:
        nombre = auxiliar_ficheros.formatoArchivo(nombreGrafica,"png")
        plt.savefig(join(Constantes.RUTA_SALIDA,nombre))

def histogramaFrecuencia(lista_valores:list,nombreGrafica = "Grafica"):
    plt.hist(lista_valores, bins=30)

    plt.xlabel('Values')
    plt.ylabel('Frecuency')
    plt.title('Histogram of values')
    plt.gca().get_yaxis().set_major_locator(plt.MaxNLocator(integer=True))
    if Constantes.RUTA_SALIDA == "":
        plt.show()
    else:
        nombre = auxiliar_ficheros.formatoArchivo(nombreGrafica,"png")
        plt.savefig(join(Constantes.RUTA_SALIDA,nombre))

def pintarVariosHistogramas(arrayHistogramas:list,arrayTitulos:list,nombreGrafica):

    rango = list(range(24))
    plt.xlabel('Time (hours)')
    plt.ylabel('Values')
    plt.title('Line Graph')
    for i in range(len(arrayHistogramas)):
        plt.plot(rango,arrayHistogramas[i],label=arrayTitulos[i])

    plt.legend()

    if Constantes.RUTA_SALIDA == "":
        plt.show()
    else:
        nombre = auxiliar_ficheros.formatoArchivo(nombreGrafica, "png")
        plt.savefig(join(Constantes.RUTA_SALIDA, nombre))
